import React, { useState } from "react";
import { View, Text, PanResponder, Pressable, StyleSheet } from "react-native";
import { Canvas, Line, useCanvasRef } from "@shopify/react-native-skia";
import { Point, Stroke } from "@/types/canvas";

function CanvasComponent() {
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

    return points
      .slice(1)
      .map((point, index) => (
        <Line
          key={`${key}-${index}`}
          p1={{ x: points[index].x, y: points[index].y }}
          p2={{ x: point.x, y: point.y }}
          color="#2c3e50"
          strokeWidth={2.5}
          strokeCap="round"
        />
      ));
  };

  return (
    <View className="flex-1 bg-background">
      {/* Canvas Container */}
      <View className="flex-1 m-2.5" {...panResponder.panHandlers}>
        <Canvas ref={canvasRef} style={styles.canvas}>
          {/* Render completed strokes */}
          {strokes.map((stroke, index) => renderStroke(stroke.points, index))}

          {/* Render current stroke */}
          {renderStroke(currentStroke, "current")}
        </Canvas>
      </View>

      {/* Button Container */}
      <View className="flex-row justify-center items-center py-5 px-5 gap-4 bg-surface">
        <Pressable
          className="px-6 py-3 rounded-lg bg-secondary active:opacity-80 active:scale-95 min-w-[100]"
          onPress={handleClear}
        >
          <Text className="text-white font-semibold text-base text-center">
            Clear
          </Text>
        </Pressable>

        <Pressable
          className="px-6 py-3 rounded-lg bg-primary active:opacity-80 active:scale-95 min-w-[100]"
          onPress={handleSave}
        >
          <Text className="text-white font-semibold text-base text-center">
            Search
          </Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  canvas: {
    flex: 1,
    backgroundColor: "#fff", // surface color
    borderRadius: 8,
    elevation: 2, // Android shadow
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
});

export default CanvasComponent;
