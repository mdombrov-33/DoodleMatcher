import { Match, Point, SearchResult, Stroke } from "@/types/canvas";
import { Line, useCanvasRef } from "@shopify/react-native-skia";
import React, { useState } from "react";
import { Alert, PanResponder } from "react-native";

export function useDrawing() {
  const canvasRef = useCanvasRef();
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [currentStroke, setCurrentStroke] = useState<Point[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [matches, setMatches] = useState<Match[]>([]);

  //! PanResponder to track finger drawing
  const panResponder = PanResponder.create({
    onStartShouldSetPanResponder: () => true,
    onMoveShouldSetPanResponder: () => true,

    onPanResponderGrant: (event) => {
      const { locationX, locationY } = event.nativeEvent;
      setIsDrawing(true);
      setCurrentStroke([{ x: locationX, y: locationY }]);
    },

    onPanResponderMove: (event) => {
      if (!isDrawing) return;
      const { locationX, locationY } = event.nativeEvent;
      setCurrentStroke((prev) => [...prev, { x: locationX, y: locationY }]);
    },

    onPanResponderRelease: () => {
      if (isDrawing && currentStroke.length > 1) {
        setStrokes((prev) => [...prev, { points: currentStroke }]);
        setCurrentStroke([]);
        setIsDrawing(false);
      }
    },
  });

  //! Reset search results
  const resetSearch = () => {
    setMatches([]);
  };

  //! Clear canvas
  const handleClear = () => {
    setStrokes([]);
    setCurrentStroke([]);
    setIsDrawing(false);
    console.log("Canvas cleared");
  };

  //! Capture canvas as base64 string
  const captureCanvas = (): string | null => {
    if (!canvasRef.current) return null;
    const image = canvasRef.current.makeImageSnapshot();
    if (!image) return null;
    return image.encodeToBase64();
  };

  //! Send base64 image to backend and get matches
  const searchDoodle = async (base64: string): Promise<SearchResult | null> => {
    setIsLoading(true);
    try {
      //* If using Android Studio emulator
      // const url = "http://10.0.2.2:8000/api/search-doodle";
      //* If using Windows
      // const url = "http://localhost:8000/api/search-doodle";
      //* If using WSL 2
      const url = "http://192.168.1.179:8000/api/search-doodle";

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image_data: base64 }),
      });
      return await response.json();
    } catch (error) {
      console.error("Error during search:", error);
      return null;
    } finally {
      setIsLoading(false);
    }
  };

  //! Validate canvas and perform search
  const handleSearch = async () => {
    if (strokes.length === 0) {
      Alert.alert(
        "There is nothing on canvas",
        "Please draw something before searching."
      );
      return null;
    }

    const base64 = captureCanvas();
    if (!base64) return null;

    console.log("Drawing captured, length:", base64.length);

    const result = await searchDoodle(base64);
    setMatches(result?.matches || []);
    console.log("Matches received:", result);
  };

  //! Render a stroke as a series of lines
  const renderStroke = (points: Point[], key: string | number) => {
    if (points.length < 2) return null;
    return (
      <React.Fragment key={key}>
        {points.slice(1).map((point, index) => (
          <Line
            key={`${key}-${index}`}
            p1={{ x: points[index].x, y: points[index].y }}
            p2={{ x: point.x, y: point.y }}
            color="#2c3e50"
            strokeWidth={2.5}
            strokeCap="round"
          />
        ))}
      </React.Fragment>
    );
  };

  return {
    strokes,
    panResponder,
    handleSearch,
    handleClear,
    canvasRef,
    currentStroke,
    renderStroke,
    isLoading,
    matches,
    resetSearch,
  };
}
