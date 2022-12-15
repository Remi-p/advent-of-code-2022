import { readFileSync } from "fs";

const input = readFileSync("./input.txt", "utf8");

const parseSensorsAndBeacons = (input: string) => {
  return input.split("\n").map((line) => {
    const parsed_line =
      /Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)/.exec(
        line
      );
    if (parsed_line === null) {
      throw new Error(`Line [${line}] parsing failed`);
    }
    const [sensor_x, sensor_y, beacon_x, beacon_y] = [
      parsed_line[1],
      parsed_line[2],
      parsed_line[3],
      parsed_line[4],
    ].map(Number);
    return { sensor_x, sensor_y, beacon_x, beacon_y };
  });
};
type ParsedSensorsAndBeacons = ReturnType<typeof parseSensorsAndBeacons>;

class Position {
  constructor(public x: number, public y: number) {}

  clone() {
    return new Position(this.x, this.y);
  }

  str() {
    return Position.str(this.x, this.y);
  }

  find() {
    return Position.find(this.x, this.y);
  }

  computeDistance(pos: Position) {
    return Math.abs(this.x - pos.x) + Math.abs(this.y - pos.y);
  }

  frequency() {
    return this.x * 4000000 + this.y;
  }

  public static str(x: number, y: number) {
    return x + "," + y;
  }

  public static find(x: number, y: number) {
    return (pos: Position) => pos.x === x && pos.y === y;
  }
}

class Grid {
  sensorsBeaconDistance: {
    [key in string]: { position: Position; beaconDistance: number };
  } = {};
  beacons: Position[] = [];
  boundaries?: { start: Position; end: Position };

  constructor(parsedSensorsAndBeacons: ParsedSensorsAndBeacons) {
    parsedSensorsAndBeacons.forEach((parsedSensorAndBeacon) => {
      const sensor = new Position(
        parsedSensorAndBeacon.sensor_x,
        parsedSensorAndBeacon.sensor_y
      );
      const beacon = new Position(
        parsedSensorAndBeacon.beacon_x,
        parsedSensorAndBeacon.beacon_y
      );
      this.extendsBoundaries(sensor);
      this.extendsBoundaries(beacon);

      this.sensorsBeaconDistance[sensor.str()] = {
        position: sensor,
        beaconDistance: sensor.computeDistance(beacon),
      };
      this.beacons.push(beacon);
    });
  }

  extendsBoundaries(pos: Position) {
    if (!this.boundaries) {
      this.boundaries = { start: pos.clone(), end: pos.clone() };
    }
    if (this.boundaries.start.x >= pos.x) {
      this.boundaries.start.x = pos.x;
    }
    if (this.boundaries.start.y >= pos.y) {
      this.boundaries.start.y = pos.y;
    }
    if (this.boundaries.end.x <= pos.x) {
      this.boundaries.end.x = pos.x;
    }
    if (this.boundaries.end.y <= pos.y) {
      this.boundaries.end.y = pos.y;
    }
  }

  getInRangeSensor(position: Position) {
    const sensorPos = Object.keys(this.sensorsBeaconDistance).find(
      (sensorPosition) => {
        const sensor = this.sensorsBeaconDistance[sensorPosition];
        return (
          sensor.position.computeDistance(position) <= sensor.beaconDistance
        );
      }
    );
    return sensorPos === undefined
      ? sensorPos
      : this.sensorsBeaconDistance[sensorPos];
  }

  hasNoBeacon(position: Position) {
    if (this.beacons.some(position.find())) {
      return false;
    }

    return this.getInRangeSensor(position) !== undefined;
  }

  countNoBeaconPositionsY(y: number) {
    if (!this.boundaries) {
      throw new Error("Boundaries need to be defined before drawing grid");
    }
    let total = 0;

    for (let x = this.boundaries.start.x; x < this.boundaries.end.x; x++) {
      const position = new Position(x, y);

      if (this.hasNoBeacon(position)) {
        total += 1;
      }
    }
    return total;
  }

  findLostBeacon(minSearch: number, maxSearch: number) {
    if (!this.boundaries) {
      throw new Error("Boundaries need to be defined before drawing grid");
    }
    for (let y = minSearch; y < maxSearch + 1; y++) {
      for (let x = minSearch; x < maxSearch + 1; x++) {
        const inspectedPos = new Position(x, y);
        const inRangeSensor = this.getInRangeSensor(inspectedPos);
        if (!inRangeSensor) {
          console.log(inspectedPos);
          return inspectedPos;
        }
        const lineCoveredByBeacon =
          inRangeSensor.beaconDistance -
          inRangeSensor.position.computeDistance(inspectedPos);
        x += lineCoveredByBeacon;
      }
      if (y % 100000 === 0) {
        console.log(`[${y}]`);
      }
    }
  }

  drawGrid() {
    if (!this.boundaries) {
      throw new Error("Boundaries need to be defined before drawing grid");
    }
    for (let y = this.boundaries.start.y; y < this.boundaries.end.y + 1; y++) {
      for (
        let x = this.boundaries.start.x;
        x < this.boundaries.end.x + 1;
        x++
      ) {
        if (Position.str(x, y) in this.sensorsBeaconDistance) {
          process.stdout.write("Ꙋ");
        } else if (this.beacons.some(Position.find(x, y))) {
          process.stdout.write("●");
        } else {
          process.stdout.write("·");
        }
      }
      process.stdout.write(" " + String(y));
      process.stdout.write("\n");
    }
  }
}

const countNoBeaconPositions = (input: string) => {
  const grid = new Grid(parseSensorsAndBeacons(input));
  // grid.drawGrid();
  console.log("countNoBeaconPositions:", grid.countNoBeaconPositionsY(2000000));
};

const distressBeaconFrequency = (input: string) => {
  const grid = new Grid(parseSensorsAndBeacons(input));
  // grid.drawGrid();
  console.log(
    "lostBeaconFrequency:",
    grid.findLostBeacon(0, 4000000)?.frequency()
  );
};

// countNoBeaconPositions(input);
distressBeaconFrequency(input);
