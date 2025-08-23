import { Tabs } from "expo-router";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { theme } from "@/constants/theme";

export default function Layout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: theme.colorPrimary,
        tabBarLabelStyle: {
          fontSize: 14,
        },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Draw",
          headerShown: true,
          tabBarShowLabel: true,
          tabBarIcon: ({ size, color }) => (
            <MaterialIcons name="draw" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="history"
        options={{
          title: "History",
          headerShown: true,
          tabBarShowLabel: true,
          tabBarIcon: ({ size, color }) => (
            <MaterialIcons name="history-edu" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
