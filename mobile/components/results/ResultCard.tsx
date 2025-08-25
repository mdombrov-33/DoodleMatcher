import { Match } from "@/types/canvas";
import { View, Text, Image } from "react-native";

type Props = {
  match: Match;
};

export default function ResultCard({ match }: Props) {
  return (
    <View className="bg-surface rounded-xl shadow-md p-4 mb-4">
      {/* Image */}
      <Image
        source={{ uri: match.photo_url }}
        className="w-full h-48 rounded-lg mb-3"
      />

      {/* Animal Type */}
      <Text className="text-text font-bold text-lg mb-1">
        {match.animal_type}
      </Text>

      {/* Confidence Bar */}
      <View className="flex-row items-center">
        <View
          className="h-2 rounded-full bg-success"
          style={{ width: `${match.confidence}%` }}
        />
        <Text className="ml-2 text-textMuted text-sm">
          {match.confidence.toFixed(1)}%
        </Text>
      </View>
    </View>
  );
}
