import { Point, Stroke } from "@/types/canvas";
import { Line, useCanvasRef } from "@shopify/react-native-skia";
import React, { useState } from "react";
import { PanResponder } from "react-native";

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
  };

  const handleSave = async () => {
    if (canvasRef.current) {
      try {
        // Convert canvas to bitmap image
        const image = canvasRef.current.makeImageSnapshot();
        if (image) {
          const base64 = image.encodeToBase64();
          console.log("Drawing saved as PNG base64, length:", base64?.length);

          const response = await fetch("URL/search-doodle", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              image: base64, // The PNG as base64 string
            }),
          });

          const matches = await response.json();
          console.log("Got matches:", matches);

          return matches;
        }
      } catch (error) {
        console.error("Error saving/searching:", error);
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
