import ResultCard from "@/components/results/ResultCard";
import ActionButton from "@/components/ActionButton";
import { ScrollView, View } from "react-native";
import { Match } from "@/types/canvas";

type Props = {
  resetSearch: () => void;
  matches: Match[];
};

export default function Results({ resetSearch, matches }: Props) {
  return (
    <View className="flex-1">
      <ScrollView>
        {matches.map((match, index) => (
          <ResultCard key={index} match={match} />
        ))}
      </ScrollView>
      <ActionButton
        title="Draw Again"
        variant="primary"
        onPress={resetSearch}
      />
    </View>
  );
}
