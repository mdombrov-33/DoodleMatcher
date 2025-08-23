import React, { useRef } from "react";
import { View, Button, Alert } from "react-native";
import { Canvas, Path, useCanvasRef } from "@shopify/react-native-skia";

const DrawCanvas = () => {
  const canvasRef = useCanvasRef(); //* Reference to the Canvas
  const pathRef = useRef(""); //* Stores the current path string

  const handleTouchStart = (event: any) => {
    const { locationX, locationY } = event.nativeEvent;
    pathRef.current = `M ${locationX} ${locationY}`; //* Start a new path
  };

  const handleTouchMove = (event: any) => {
    const { locationX, locationY } = event.nativeEvent;
    pathRef.current += ` L ${locationX} ${locationY}`; //* Add a line to the path
    console.log("Updated Path:", pathRef.current);
    canvasRef.current?.redraw(); //* Trigger a redraw of the canvas
  };

  const handleExport = () => {
    const image = canvasRef.current?.makeImageSnapshot();
    if (image) {
      const bytes = image.encodeToBytes(); //* Convert to Uint8Array
      console.log("Image bytes:", bytes);
      Alert.alert("Export Successful", "The canvas has been exported!");
    } else {
      Alert.alert("Export Failed", "Could not capture the canvas.");
    }
  };

  return (
    <View className="flex-1">
      <View
        className="flex-1"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
      >
        <Canvas ref={canvasRef} className="flex-1 bg-white">
          <Path path={pathRef.current} color="black" strokeWidth={2} />
        </Canvas>
      </View>
      <Button title="Export Canvas" onPress={handleExport} />
    </View>
  );
};

export default DrawCanvas;
