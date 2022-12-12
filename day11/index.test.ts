import { predictMonkeyMoves } from ".";
import { readFileSync } from "fs";

const trainingInput = readFileSync("./inputs/traininginput.txt", "utf8");

const input = readFileSync("./inputs/input.txt", "utf8");

describe("Should predict monkey moves", () => {
  describe("Training input", () => {
    it("predicts based on training input", () => {
      expect(predictMonkeyMoves(trainingInput)).toEqual({
        levelOfMonkeyBusiness: 10605,
      });
    });
    it("predicts with lot of worries", () => {
      expect(predictMonkeyMoves(trainingInput, true)).toEqual({
        levelOfMonkeyBusiness: 2713310158,
      });
    });
  });

  describe("Actual input", () => {
    it("predicts based on actual input", () => {
      expect(predictMonkeyMoves(input)).toEqual({
        levelOfMonkeyBusiness: 90294,
      });
    });
    it("predics with lot of worries", () => {
      expect(predictMonkeyMoves(input, true)).toEqual({
        levelOfMonkeyBusiness: 18170818354,
      });
    });
  });
});
