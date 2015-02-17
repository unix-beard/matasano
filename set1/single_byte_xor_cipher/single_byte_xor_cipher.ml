(********************************************************************************
* The matasano crypto challenges
* http://cryptopals.com/sets/1/challenges/3/
* Set 1   Challenge 3
* Single byte XOR cipher
*
* Compile it like this:
* $ ocamlfind ocamlc -package batteries -linkpkg -o single_byte_xor_cipher single_byte_xor_cipher.ml
*
* And run it like this:
* $ ./single_byte_xor_cipher | grep -a "Cooking MC's like a pound of bacon"
********************************************************************************
* The hex encoded string:
* 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
* has been XOR'd against a single character. Find the key, decrypt the message.
* Key:      int=88, char='X'
* Message:  Cooking MC's like a pound of bacon
*******************************************************************************)

open Batteries

let normalize s =
    let make_hex_str i (*index*) =
        let prev = String.get s (i - 1)
        and cur = String.get s i
        in
        ("0x" ^ String.make 1 prev) ^ (String.make 1 cur)
    in
    let pair_elem i ch =
        if i mod 2 <> 0 && i <> 0 then
            let hex = int_of_string (make_hex_str i) in char_of_int hex
        else
            Char.chr 0
    in
    BatString.filter ((<>) (Char.chr 0)) (BatString.mapi pair_elem s)

let int_from_hex_char ch =
    BatInt.of_string ("0x" ^ (BatString.make 1 ch))

let xor_chars a b =
    Char.chr ((Char.code a) lxor b)

let rec decode key s =
    if key < 256 then decode_with_key key s
and decode_with_key key s =
    Printf.printf "[*] Trying the key: int: %d, char: %C\n" key (Char.chr key);
    Printf.printf "Decoded message: %s\n" (BatString.map (fun ch -> xor_chars ch key) s);
    decode (key + 1) s

let () =
    (* Our hex encoded string *)
    let e = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    in
    (* Our 'normalized' string *)
    let n = normalize e in decode 0 n 
