use std::env;
use std::fs;

/*
 A = (X) = Rock
 B = (Y) = Paper
 C = (Z) = Scissors
*/

// ----- Part One

// fn shape_score(shape: &str) -> i32 {
//     match shape {
//         "X" => return 1,
//         "Y" => return 2,
//         "Z" => return 3,
//         _ => panic!("Shape score unknown"),
//     }
// }

// fn match_score(match_value: &str) -> i32 {
//     match match_value {
//         "A X" => return 3,
//         "A Y" => return 6,
//         "A Z" => return 0,
//         "B X" => return 0,
//         "B Y" => return 3,
//         "B Z" => return 6,
//         "C X" => return 6,
//         "C Y" => return 0,
//         "C Z" => return 3,
//         _ => panic!("Match score unknown"),
//     }
// }

// ----- Part Two
// (function names should actually be inverted)

fn shape_score(shape: &str) -> i32 {
    match shape {
        "X" => return 0,
        "Y" => return 3,
        "Z" => return 6,
        _ => panic!("Shape score unknown"),
    }
}

fn match_score(match_value: &str) -> i32 {
    match match_value {
        "A X" => return 3,
        "A Y" => return 1,
        "A Z" => return 2,
        "B X" => return 1,
        "B Y" => return 2,
        "B Z" => return 3,
        "C X" => return 2,
        "C Y" => return 3,
        "C Z" => return 1,
        _ => panic!("Match score unknown"),
    }
}

fn main() {
    // --snip--
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut total_score = 0;

    for line in contents.split("\n") {
        let vec: Vec<&str> = line.split(" ").collect();
        let choosen_shape = vec[1];
        total_score = total_score + shape_score(choosen_shape) + match_score(line);
    }
    println!("Total score = {}", total_score);
}
