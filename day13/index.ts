import { readFileSync } from "fs";

const input = readFileSync("./input.txt", "utf8");

enum ComparisonResult {
  UNCLEAR,
  UNORDERED,
  ORDERED,
}

type Packet = Array<number | Packet>;

const convertToArray = (packet: Packet, indice: number) => {
  return Array.isArray(packet[indice])
    ? (packet[indice] as Packet)
    : [packet[indice]];
};

const compareArraysOfNumber = (
  left: Packet,
  right: Packet
): ComparisonResult => {
  for (let i = 0; i < Math.max(left.length, right.length); i++) {
    if (right[i] === undefined) {
      return ComparisonResult.UNORDERED;
    }
    if (left[i] === undefined) {
      return ComparisonResult.ORDERED;
    }
    if (Array.isArray(left[i]) || Array.isArray(right[i])) {
      const leftValue = convertToArray(left, i);
      const rightValue = convertToArray(right, i);
      const subResult = compareArraysOfNumber(leftValue, rightValue as Packet);
      if (subResult !== ComparisonResult.UNCLEAR) {
        return subResult;
      }
    } else if (left[i] !== right[i]) {
      return left[i] < right[i]
        ? ComparisonResult.ORDERED
        : ComparisonResult.UNORDERED;
    }
  }
  return ComparisonResult.UNCLEAR;
};

const checkPackets = (input: string) => {
  const conditionResults = input.split("\n\n").map((pair) => {
    const [left, right] = pair.split("\n").map((side) => JSON.parse(side));
    return compareArraysOfNumber(left, right);
  });

  const rightOrderIndicesSum = conditionResults.reduce(
    (acc, value, idx) =>
      value !== ComparisonResult.UNORDERED ? acc + idx + 1 : acc,
    0
  );

  console.log("Sum of pair indices in the right order:", rightOrderIndicesSum);
};

const orderPackets = (input: string) => {
  const DIVIDER_PACKET1 = [[2]];
  const DIVIDER_PACKET2 = [[6]];
  const packets: Packet[] = input
    .replaceAll("\n\n", "\n")
    .split("\n")
    .map((jsonPacket) => JSON.parse(jsonPacket));

  packets.push(DIVIDER_PACKET1, DIVIDER_PACKET2);

  packets.sort((packetA, packetB) => {
    return compareArraysOfNumber(packetA, packetB) !==
      ComparisonResult.UNORDERED
      ? -1
      : 1;
  });

  const findIndex = (compareTo: Packet) => (value: Packet) =>
    compareArraysOfNumber(value, compareTo) === ComparisonResult.UNCLEAR;

  const firstPacketIdx = packets.findIndex(findIndex(DIVIDER_PACKET1)) + 1;
  const secndPacketIdx = packets.findIndex(findIndex(DIVIDER_PACKET2)) + 1;

  console.log(`The decoder key is ${firstPacketIdx * secndPacketIdx}`);
};

checkPackets(input);
orderPackets(input);
