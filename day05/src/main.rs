const INPUT: &str = include_str!("../input.txt");
fn main() {
    let mut parts = INPUT.split("\n\n");
    let mut crates = parts
        .next()
        .unwrap()
        .split("\n")
        .collect::<Vec<&str>>()
        .into_iter()
        .rev();
    let movements = parts.next().unwrap().split("\n");

    let mut stacks: Vec<Vec<char>> = Vec::new();

    // Init stacks
    crates.next().unwrap().chars().for_each(|stack_index| {
        if stack_index != ' ' {
            stacks.push(Vec::new());
        }
    });

    crates.for_each(|crate_line| {
        for i in 0..stacks.len() {
            let current_crate = crate_line.chars().nth(position_from_index(i)).unwrap();
            if current_crate != ' ' {
                // NOT stacks.get(i).unwrap().push(currentCrate);
                stacks[i].push(current_crate);
            }
        }
    });

    for movement in movements {
        let movement_instructions = movement.split(" ").collect::<Vec<&str>>();
        let quantity = movement_instructions[1].parse::<usize>().unwrap();
        let from = movement_instructions[3].parse::<usize>().unwrap();
        let to = movement_instructions[5].parse::<usize>().unwrap();

        crate_mover_9001(&mut stacks, quantity, from, to);
    }

    let top_crates = stacks
        .iter()
        .map(|stack| stack.last().unwrap().clone())
        .collect::<String>();

    println!("Crates at the top: {}", top_crates);
}

fn position_from_index(index: usize) -> usize {
    return index * 4 + 1;
}

fn crate_mover_9000(stacks: &mut Vec<Vec<char>>, quantity: usize, from: usize, to: usize) {
    for _ in 0..quantity {
        let moved_crate = stacks[from - 1].pop().unwrap().clone();
        stacks[to - 1].push(moved_crate);
    }
}

fn crate_mover_9001(stacks: &mut Vec<Vec<char>>, quantity: usize, from: usize, to: usize) {
    let mut unloading_area: Vec<char> = Vec::new();
    for _ in 0..quantity {
        let moved_crate = stacks[from - 1].pop().unwrap().clone();
        unloading_area.push(moved_crate)
    }
    for _ in 0..quantity {
        stacks[to - 1].push(unloading_area.pop().unwrap().clone());
    }
}
