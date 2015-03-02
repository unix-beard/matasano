(*******************************************************************************
* The matasano crypto challenges
* http://cryptopals.com/sets/1/challenges/4/
* Set 1   Challenge 4
* Detect single-character XOR
* Compile it like this:
* $ ocamlfind ocamlc -package batteries,core,forkwork -thread -linkpkg 
*   -o parallel_detect_single_character_xor parallel_detect_single_character_xor.ml
********************************************************************************
* One of the 60-character strings in the input file has been encrypted 
* by single-character XOR. Find it. 
* Key:      int=53, char='5'
* Message:  Now that the party is jumping
*
* NOTE: This implementation is parallel (requires ForkWork package)
*******************************************************************************)

open Core.Std
open Batteries

let tmp_files = RefList.empty ()
let _workers = ref 1


(*******************************************************************************
 * FILE SPLITTING LOGIC - BEGIN 
 ******************************************************************************)
let prelim_calculations number_of_workers filename =
    (* Calculate total file size and split file size
     * (total_file_size / number_of_workers) in bytes
     *)
    let total_file_size = File.size_of filename in
    total_file_size / number_of_workers

let line_stream_of_channel channel =
    Stream.from
      (fun _ ->
         try Some (input_line channel) with End_of_file -> None)

let rec write_line out stream bytes_read_so_far split_file_size =
    if bytes_read_so_far < split_file_size then
        let line = (Stream.next stream) ^ "\n" in
        String.print out line;
        write_line out stream (bytes_read_so_far + (String.length line)) split_file_size

let make_tmp stream split_file_size =
    File.with_temporary_out ~suffix:".tmp"
        (fun out name -> RefList.add tmp_files name; write_line out stream 0 split_file_size)

let rec process_stream stream workers split_file_size =
    if workers > 0 then begin
        make_tmp stream split_file_size;
        ignore (process_stream stream (workers - 1) split_file_size)
    end

let read_file workers filename () =
    let in_chan = open_in filename in
    let split_file_size = prelim_calculations workers filename in
    let stream = line_stream_of_channel in_chan in
    try
        _workers := workers;
        process_stream stream !_workers split_file_size;
        close_in in_chan
    with e ->
        (*RefList.iter (fun f -> print_endline(f)) tmp_files;*)
        close_in in_chan

(*******************************************************************************
 * FILE SPLITTING LOGIC - END 
 ******************************************************************************)


(*******************************************************************************
 * DECODING LOGIC - BEGIN
 ******************************************************************************)

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

let rec decode key s results filename =
    if key < 256 then decode_with_key key s results filename
and decode_with_key key s results filename =
    let decoded_msg = BatString.map (fun ch -> xor_chars ch key) s in
    let readable = is_readable decoded_msg in
        if readable then 
            begin
                (*Printf.printf "[*] Trying the key: %d, char: %C\nDecoded message: %s\n" key (Char.chr key) decoded_msg;*)
                RefList.add results (decoded_msg, key, filename);
                decode (key + 1) s results filename
            end
        else
            decode (key + 1) s results filename

let decode_file filename =
    let filelines = File.lines_of filename in
    let results = RefList.empty () in
    Enum.iter (fun line -> (*Printf.printf "File: %s; Decoding [%s]\n" filename line;*) decode 0 (normalize line) results filename) filelines;
    RefList.to_list results

(*******************************************************************************
 * DECODING LOGIC - END
 ******************************************************************************)


let command =
    Command.basic
        ~summary:"Parallel detect single-character XOR - OCaml implementation"
        ~readme:(fun () -> "Matasano crypto challenge: set 1, challange 4")
        Command.Spec.(
            empty 
            +> flag "-w" (optional_with_default 1 int) ~doc:"Number of workers"
            +> anon ("filename" %: string))
        read_file

let print_results results = 
    List.iter (fun (m, k, f) -> Printf.printf "Possible decoded message (key=%C, file=%s):\n%s\n" (Char.chr k) f m) results

let split_work workers =
    Printf.printf "Number of workers: %d\n" workers;
    let list_of_files = RefList.to_list tmp_files in
    let results = ForkWork.map_list decode_file list_of_files in
    print_results (List.flatten results)


let () = 
    (* Step #1: Split input file into multiple smaller files *)
    Command.run ~version:"1.0" ~build_info:"RWO" command;
    (* Step #2: Spawn one worker process per file and collect the results *)
    split_work !_workers 
