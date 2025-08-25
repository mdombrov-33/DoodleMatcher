import { Pressable, Text } from "react-native";

type Props = {
  title: string;
  onPress: () => void;
  variant?: "primary" | "secondary";
  className?: string;
};

export default function ActionButton({
  title,
  onPress,
  variant = "primary",
  className,
}: Props) {
  const baseClasses =
    "px-6 py-3 rounded-lg active:opacity-80 active:scale-95 min-w-[100]";
  const variantClasses = variant === "primary" ? "bg-primary" : "bg-secondary";

  return (
    <Pressable
      className={`${baseClasses} ${variantClasses} ${className || ""}`}
      onPress={onPress}
    >
      <Text className="text-white font-semibold text-base text-center">
        {title}
      </Text>
    </Pressable>
  );
}
