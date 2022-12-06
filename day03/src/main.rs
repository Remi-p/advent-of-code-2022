use std::env;
use std::fs;

fn main() {
    // day1();
    day2();
}

fn day1() {
    // --snip--
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let scores: &str = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";

    let total: usize = contents
        .lines()
        .map(|line| {
            let (compartment1, compartment2) = line.split_at(line.chars().count() / 2);
            // dbg!(compartment1, compartment2);
            for char in compartment1.chars() {
                if compartment2.find(char) != None {
                    return char;
                }
            }
            return '!';
        })
        .map(|char| scores.chars().position(|c| c == char).unwrap())
        .sum();
    println!("Total for day1 = {}", total);
}

fn char_score(char: char) -> usize {
    let scores: &str = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    scores.chars().position(|c| c == char).unwrap()
}

fn day2() {
    // --snip--
    let args: Vec<String> = env::args().collect();
    let file_path = &args[1];
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut lines = contents.split("\n");
    let mut line = lines.next();
    let mut total = 0;
    while line != None {
        let elf1 = line.unwrap();
        let elf2 = lines.next().unwrap();
        let elf3 = lines.next().unwrap();
        line = lines.next();
        for char in elf1.chars() {
            if elf2.find(char) != None && elf3.find(char) != None {
                total += char_score(char);
                break;
            }
        }
    }
    println!("Total for day2 = {}", total)
}
