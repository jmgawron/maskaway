# maskaway
The purpose of this script is to help protect critical information in logs and debug outputs by hiding the real values of IPs and MAC addresses. It is designed to support troubleshooting processes in environments where preserving the confidentiality of original MAC and IP addresses is essential. The script replaces the actual values with artificial ones, maintaining the correlation in the replacement process to ensure consistency.

# usage:

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



# additional considerations:

- The script detects MAC addresses, IPv4, and IPv6 addresses.
- Supported MAC address formats include both `xxxx.xxxx.xxxx` and `xx:xx:xx:xx:xx:xx`.
- Multiple files can be imported.
- The two-phase process separates the discovery of used MAC addresses from the replacement stage.
- Original input files remain unmodified.
- The IP address `0.0.0.0` is the only unmodified IP address to retain its designation as invalid, often indicating a deviation from expected software behavior.
- The support team receives only the `.modified` file, while the `swap.map` and original files remain with the end customer and are not shared.
- If the support team identifies issues in the modified outputs, they will make conclusions based on the modified values. By sharing this information with the end customer, the customer can use the `swap.map` file to trace problematic values back to the original ones.

