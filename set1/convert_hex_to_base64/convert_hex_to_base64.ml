(*******************************************************************************
* The matasano crypto challenges
* http://cryptopals.com/sets/1/challenges/1/
* Set 1   Challenge 1
* Convert hex to base64
* Compile it like this:
* $ ocamlfind ocamlc -package base64,batteries -o hexbase64 -linkpkg convert_hex_to_base64.ml
********************************************************************************
* The string:
* 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d
* Should produce:
* SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
*******************************************************************************)
open Batteries
open B64
 
let s = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
and k = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
 
let pair_elem i ch =
    if i mod 2 <> 0 && i <> 0 then
        let hex = int_of_string ("0x" ^ String.make 1 (String.get s (i - 1)) ^ String.make 1 (String.get s i)) in
        char_of_int hex
    else 
        Char.chr 0
 
let () =
    let decoded_str = BatString.filter ((<>) (Char.chr 0)) (BatString.mapi pair_elem s) in
    assert ((B64.encode decoded_str) = k)
