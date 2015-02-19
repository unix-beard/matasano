(*******************************************************************************
* The matasano crypto challenges
* http://cryptopals.com/sets/1/challenges/4/
* Set 1   Challenge 4
* Detect single-character XOR
* Compile it like this:
* $ ocamlfind ocamlc -package batteries -linkpkg -o detect_single_character_xor detect_single_character_xor.ml 
********************************************************************************
* One of the 60-character strings in the input file has been encrypted 
* by single-character XOR. Find it. 
* Key:      int=53, char='5'
* Message:  Now that the party is jumping
*
* NOTE: This implementation is strictly sequential
*******************************************************************************)

open Batteries

let normalize s =
    let make_hex_str i (*index*) =
        let prev = String.get s (i - 1)
        and cur  = String.get s i in
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

let is_readable msg = 
    (* Determines if msg is readable 
     * (i.e., consists of printable ascii characters)
     *)
    let r1 = BatChar.range ' '  ~until:'~'
    and r2 = BatChar.range '\n' ~until:'\n' in
    let merged = List.of_enum (BatEnum.merge (fun _ _ -> true) r1 r2) in
    BatEnum.for_all (fun c -> List.mem c merged) (BatString.enum msg)

let rec decode key s =
    if key < 256 then decode_with_key key s
and decode_with_key key s =
    let decoded_msg = BatString.map (fun ch -> xor_chars ch key) s in
    let readable = is_readable decoded_msg in
        if readable then
            Printf.printf "[*] Trying the key: %d, char: %C\nDecoded message: %s\n" key (Char.chr key) decoded_msg;
        decode (key + 1) s

let () =
    let filelines = File.lines_of "4.txt" in
    Enum.iter (fun line -> Printf.printf "Decoding [%s]\n" line; decode 0 (normalize line)) filelines 
