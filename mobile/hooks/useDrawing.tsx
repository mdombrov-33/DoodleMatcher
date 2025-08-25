import { Point, Stroke } from "@/types/canvas";
import { Line, useCanvasRef } from "@shopify/react-native-skia";
import React, { useState } from "react";
import { Alert, PanResponder } from "react-native";

export function useDrawing() {
  const canvasRef = useCanvasRef();
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [currentStroke, setCurrentStroke] = useState<Point[]>([]);
  const [isDrawing, setIsDrawing] = useState(false);

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

  const handleClear = () => {
    setStrokes([]);
    setCurrentStroke([]);
    setIsDrawing(false);
    console.log("Canvas cleared");
  };

  const handleSave = async () => {
    if (strokes.length === 0) {
      Alert.alert(
        "There is nothing on canvas",
        "Please draw something before searching."
      );
    }
    if (canvasRef.current) {
      try {
        const image = canvasRef.current.makeImageSnapshot();
        if (image) {
          const base64 = image.encodeToBase64();
          console.log("Drawing saved, length:", base64?.length);

          //! If using Android Studio emulator
          // "http://10.0.2.2:8000/api/search-doodle",
          //! If using Windows
          // "http://localhost:8000/api/search-doodle",
          //! If using WSL 2
          const response = await fetch(
            "http://192.168.1.179:8000/api/search-doodle",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ image_data: base64 }),
            }
          );

          const matches = await response.json();
          console.log("Matches received:", matches);
          return matches;
        }
      } catch (error) {
        console.error("Error during save/search:", error);
      }
    }
  };

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
    handleSave,
    handleClear,
    canvasRef,
    currentStroke,
    renderStroke,
  };
}
