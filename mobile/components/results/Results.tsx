import ResultCard from "@/components/results/ResultCard";
import ActionButton from "@/components/ActionButton";
import { View } from "react-native";

type Props = {
  resetSearch: () => void;
};

export default function Results({ resetSearch }: Props) {
  return (
    <View>
      <ResultCard />
      <ActionButton
        title="Draw Again"
        variant="primary"
        onPress={resetSearch}
      />
    </View>
  );
}
