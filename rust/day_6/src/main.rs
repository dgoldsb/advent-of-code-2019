extern crate reqwest;
use std::collections::HashMap;


fn main() -> Result<(), Box<dyn std::error::Error>> {
    let resp: String = reqwest::get("https://adventofcode.com/2019/day/6/input");
    println!("{:#?}", resp);
    Ok(())
}
