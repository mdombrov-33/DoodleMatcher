import React, { useState, useCallback } from "react";
import { View, Image, FlatList } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect } from "@react-navigation/native";
import { DrawingHistoryItem } from "@/types/history";

export default function DrawingHistory() {
  const [history, setHistory] = useState<DrawingHistoryItem[]>([]);

  const loadHistory = useCallback(async () => {
    const data = await AsyncStorage.getItem("drawingHistory");
    setHistory(data ? JSON.parse(data) : []);
  }, []);

  useFocusEffect(
    useCallback(() => {
      loadHistory();
    }, [loadHistory])
  );

  return (
    <FlatList
      data={history}
      keyExtractor={(item, idx) => item.id || idx.toString()}
      renderItem={({ item }) => (
        <View className="flex-row items-center m-2 p-2 bg-surface rounded-lg border border-border">
          <Image
            source={{ uri: `data:image/png;base64,${item.canvas}` }}
            className="w-32 h-32 mr-36 rounded bg-background"
          />
          <Image
            source={{ uri: item.result }}
            className="w-32 h-32 rounded bg-background"
          />
        </View>
      )}
      contentContainerStyle={{ padding: 8 }}
    />
  );
}
