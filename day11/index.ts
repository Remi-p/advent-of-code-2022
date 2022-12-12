const OLD = "OLD";

type Operand = number | typeof OLD;
type OperationSymbol = "*" | "+";

type Monkey = {
  position: number; // This is also the position in the array actually
  items: number[];
  inspectCount: number;
  operation: {
    symbol: OperationSymbol;
    operand1: Operand;
    operand2: Operand;
  };
  condition: {
    modulo: number;
    ifTrueMonkey: number;
    ifFalseMonkey: number;
  };
};

const monkeyExtractor = (input: string): Monkey[] => {
  return input.split("\n\n").map((monkeyString) => {
    const monkeyDetails = monkeyString.split("\n");

    const monkeyPosition = /Monkey ([0-9]):/.exec(monkeyDetails[0])![1];
    const monkeyItems = monkeyDetails[1].split(": ")[1].split(", ");
    const operation = monkeyDetails[2].split(" = ")[1].split(" ");
    const modulo = monkeyDetails[3].split(" ").pop();
    const ifTrueThrowTo = monkeyDetails[4].split(" ").pop();
    const ifFalseThrowTo = monkeyDetails[5].split(" ").pop();

    if (operation[1] !== "*" && operation[1] !== "+") {
      throw new Error(`Operation [${operation[1]}] not implemented`);
    }

    return {
      position: Number(monkeyPosition),
      items: monkeyItems.map(Number),
      inspectCount: 0,
      operation: {
        operand1: operation[0] === "old" ? OLD : Number(operation[0]),
        symbol: operation[1],
        operand2: operation[2] === "old" ? OLD : Number(operation[2]),
      },
      condition: {
        modulo: Number(modulo),
        ifTrueMonkey: Number(ifTrueThrowTo),
        ifFalseMonkey: Number(ifFalseThrowTo),
      },
    };
  });
};

const doOperation = (
  operand1: number,
  operation: OperationSymbol,
  operand2: number
) => {
  switch (operation) {
    case "*":
      return operand1 * operand2;
    case "+":
      return operand1 + operand2;
    default:
      throw new Error("Operation not implemented");
  }
};

const getOperand = (operand: Operand, item: number) => {
  if (operand === OLD) {
    return item;
  }
  return operand;
};

const calculateNewWorryLevel = (
  item: number,
  monkey: Monkey,
  commonDivider: number,
  worried: boolean
) => {
  monkey.inspectCount += 1;
  const newWorryLevel =
    doOperation(
      getOperand(monkey.operation.operand1, item),
      monkey.operation.symbol,
      getOperand(monkey.operation.operand2, item)
    ) % commonDivider;

  return worried ? newWorryLevel : Math.floor(newWorryLevel / 3);
};

const animateMonkeys = (monkeys: Monkey[], worried: boolean) => {
  const commonDivider = monkeys.reduce((acc, monkey) => {
    return acc * monkey.condition.modulo;
  }, 1);

  monkeys.forEach((monkey) => {
    while (monkey.items.length > 0) {
      const item = calculateNewWorryLevel(
        monkey.items.shift() as number,
        monkey,
        commonDivider,
        worried
      );
      const throwToMonkey =
        item % monkey.condition.modulo === 0
          ? monkey.condition.ifTrueMonkey
          : monkey.condition.ifFalseMonkey;
      monkeys[throwToMonkey].items.push(item);
    }
  });
};

export const predictMonkeyMoves = (input: string, worried = false) => {
  const ROUNDS = worried ? 10000 : 20;

  const monkeys = monkeyExtractor(input);

  for (let i = 0; i < ROUNDS; i++) {
    animateMonkeys(monkeys, worried);
  }

  monkeys.sort(
    (monkeyA, monkeyB) => monkeyB.inspectCount - monkeyA.inspectCount
  );

  return {
    levelOfMonkeyBusiness: monkeys[0].inspectCount * monkeys[1].inspectCount,
  };
};
