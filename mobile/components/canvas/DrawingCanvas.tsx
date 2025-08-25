import { View } from "react-native";
import ActionButton from "@/components/ActionButton";
import SketchArea from "@/components/canvas/SketchArea";
import { useDrawing } from "@/hooks/useDrawing";
import Results from "@/components/results/Results";

export default function DrawingCanvas() {
  const {
    canvasRef,
    panResponder,
    strokes,
    renderStroke,
    currentStroke,
    handleClear,
    handleSearch,
    isLoading,
    matches,
    resetSearch,
  } = useDrawing();

  if (matches.length > 0) {
    return <Results matches={matches} resetSearch={resetSearch} />;
  }

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
        <ActionButton
          title={isLoading ? "Searching..." : "Search"}
          onPress={handleSearch}
        />
      </View>
    </View>
  );
}
