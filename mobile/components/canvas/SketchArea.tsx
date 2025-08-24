import { Point, Stroke } from "@/types/canvas";
import { Canvas } from "@shopify/react-native-skia";
import React from "react";
import { PanResponderInstance, StyleSheet, View } from "react-native";

type Props = {
  panResponder: PanResponderInstance;
  canvasRef: React.RefObject<any>;
  strokes: Stroke[];
  renderStroke: (
    points: Point[],
    key: string | number
  ) => React.JSX.Element | null;
  currentStroke: Point[];
};

export default function SketchArea({
  panResponder,
  canvasRef,
  strokes,
  renderStroke,
  currentStroke,
}: Props) {
  return (
    <View className="flex-1 m-2.5" {...panResponder.panHandlers}>
      <Canvas ref={canvasRef} style={styles.canvas}>
        {/* Render completed strokes */}
        {strokes.map((stroke, index) => renderStroke(stroke.points, index))}

        {/* Render current stroke */}
        {renderStroke(currentStroke, "current")}
      </Canvas>
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
