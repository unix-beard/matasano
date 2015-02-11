(*******************************************************************************
* The matasano crypto challenges
* http://cryptopals.com/sets/1/challenges/2/
* Set 1   Challenge 2
* Fixed XOR
* Compile it like this:
* $ ocamlfind ocamlc -package batteries -o fixed_xor -linkpkg fixed_xor.ml
********************************************************************************
* Write a function that takes two equal-length buffers and produces their 
* XOR combination.
* If your function works properly, then when you feed it the string:
* 1c0111001f010100061a024b53535009181c
* ... after hex decoding, and when XOR'd against:
* 686974207468652062756c6c277320657965
* ... should produce:
* 746865206b696420646f6e277420706c6179
*******************************************************************************)

let decode a b =
    let m = BatInt.of_string ("0x" ^ (BatString.make 1 a))
    and n = BatInt.of_string ("0x" ^ (BatString.make 1 b))
    in
    (Printf.sprintf "%x" (m lxor n)).[0]

let fixed_xor s1 s2 =
    assert ((BatString.length s1) = (BatString.length s2));
    BatString.of_list (BatList.map2 decode (BatString.to_list s1) (BatString.to_list s2))

let () =
    let s1 = "1c0111001f010100061a024b53535009181c"
    and s2 = "686974207468652062756c6c277320657965"
    and r  = "746865206b696420646f6e277420706c6179"
    in
    assert ((fixed_xor s1 s2) = r)
    (*print_endline (fixed_xor s1 s2)*)
