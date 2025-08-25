import { Match } from "@/types/canvas";
import { Text, View } from "react-native";

type Props = {
  match: Match;
};

export default function ResultCard({ match }: Props) {
  return (
    <View>
      <Text>{match.photo_url}</Text>
    </View>
  );
}
