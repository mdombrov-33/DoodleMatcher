import { View } from "react-native";
import ActionButton from "@/components/canvas/ActionButton";
import SketchArea from "@/components/canvas/SketchArea";
import { useDrawing } from "@/hooks/useDrawing";

export default function DrawingCanvas() {
  const {
    canvasRef,
    panResponder,
    strokes,
    renderStroke,
    currentStroke,
    handleClear,
    handleSave,
  } = useDrawing();

  return (
    <View className="flex-1 bg-background">
      {/* Canvas Container */}
      <SketchArea
        panResponder={panResponder}
        canvasRef={canvasRef}
        strokes={strokes}
        renderStroke={renderStroke}
        currentStroke={currentStroke}
      />
      {/* Button Container */}
      <View className="flex-row justify-center items-center py-5 px-5 gap-4 bg-surface">
        <ActionButton title="Clear" onPress={handleClear} variant="secondary" />
        <ActionButton title="Search" onPress={handleSave} />
      </View>
    </View>
  );
}
