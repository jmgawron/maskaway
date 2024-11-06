# maskaway
The purpose of this script is to help protect critical information in logs and debug outputs by hiding the real values of IPs and MAC addresses. It is designed to support troubleshooting processes in environments where preserving the confidentiality of original MAC and IP addresses is essential. The script replaces the actual values with artificial ones, maintaining the correlation in the replacement process to ensure consistency.

# usage

**Phase One: Analysis and Mapping Creation**

In the first phase, script analyze all the IPs and MAC addresses in the provided log or debug output and build a mapping between the real values and their replacements.

Example:
```bash
python maskaway.py -analyze -input showtech.txt
swap.map has been created with artificial addresses.
```
As a result, the user receives a `swap.map` file, which contains a mapping of the original values and their corresponding replacements for the next phase.



**Phase Two: Sanitization**

In the second phase, the script sanitize the original input text file by applying the mapping dictionary to replace the real values with the artificial ones.

Example:
```bash
python maskaway.py -sanitize -dictionary swap.map -input showtech.txt
showtech.txt.modified has been created with sanitized addresses.
```
The modified version of the input file is saved with the same name, but with the `.modified` extension.



