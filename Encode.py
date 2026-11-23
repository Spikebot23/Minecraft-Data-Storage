import struct
from pathlib import Path
import shutil
import anvil


WORLD_PATH = Path(__file__).parent / "DataStorage_Save"
REGION_PATH = WORLD_PATH / "dimensions" / "minecraft" / "overworld" / "region"

EncodedBlocks = ["air","red_stained_glass", "orange_stained_glass", "yellow_stained_glass","lime_stained_glass","green_stained_glass","cyan_stained_glass","light_blue_stained_glass","purple_stained_glass","pink_stained_glass"]
OnesData = []
TensData = []
HundredsData = []

DataList = []

# Keep loaded regions in memory so we do not read the same file over and over.
regions: dict[tuple[int, int], anvil.Region] = {}


def getBlock(x: int, y: int, z: int) -> str:

    #defines what region to load based on the cordintes of the block
    region_x = x // 512
    region_z = z // 512
    region_key = (region_x, region_z)       #dictates which region file to load

    #defines what chunk to load based on the cordintes of the block
    chunk_x = x // 16
    chunk_z = z // 16
    chunk_key = (chunk_x, chunk_z)         #dictates which chunk to load

    # If the region is not loaded, load it
    if region_key not in regions:
        region_file = REGION_PATH / f"r.{region_x}.{region_z}.mca"
        regions[region_key] = anvil.Region.from_file(str(region_file))

    
    chunk = regions[region_key].get_chunk(*chunk_key)                   #Not known before:  * <-- unpacks the tuple into two arguments for the get_chunk method
    section = chunk.get_section(0)                #Get the section of the chunk that contains the block at the given Y coordinate

    # Check if the section exists and has block states.
    if section is not None and "block_states" in section:
        block_states = section["block_states"]
        palette = block_states["palette"]

        # If every block in this section is the same, there is no index array.
        if palette and isinstance(palette[0].value, str):
            if len(palette) == 1:
                return palette[0].value.split(":")[-1]

            # Otherwise, several palette indexes are packed into 64-bit numbers.
            # Find this block's position in the section (blocks are stored in Y, then Z, then X order).
            block_index = ((y % 16) * 256 + (z % 16) * 16 + (x % 16))
            
            bits_per_block = max(4, (len(palette) - 1).bit_length())
            blocks_per_long = 64 // bits_per_block
            packed_index = block_index // blocks_per_long
            position_in_long = block_index % blocks_per_long

            # Shift this block's bits to the right, then mask off the other bits.
            packed_value = block_states["data"].value[packed_index]
            palette_index = (
                packed_value >> (position_in_long * bits_per_block)
            ) & ((1 << bits_per_block) - 1)
            return palette[palette_index].value.split(":")[-1]

    # For older world formats, let Anvil handle the block lookup.
    local_x = x % 16
    local_z = z % 16
    return chunk.get_block(local_x, y, local_z).id

def getData():
    i = 0
    while getBlock(i % 256, 5, i // 256) != "redstone_block":
        x = i % 256
        z = i // 256
        OnesData.append(EncodedBlocks.index(getBlock(x, 0, z)))
        TensData.append(EncodedBlocks.index(getBlock(x, 1, z)))
        HundredsData.append(EncodedBlocks.index(getBlock(x, 2, z)))
        i+=1
        #print(x)

def decode():
    for i in range(len(HundredsData)):
        data=((HundredsData[i]*100) + (TensData[i]*10) + (OnesData[i]))
        DataList.append(data)
    payload = bytes(DataList)
    temp = "".join(chr(number) for number in payload[0:4])
    if temp != "EMRS":
        raise ValueError("World encrypted text does not match the encryption marker.")

    FlnmLen, DatLen = struct.unpack_from(">BI",payload,4 )

    name_start = 9
    data_start = name_start + FlnmLen
    data_end = data_start + DatLen

    filename = payload[name_start:data_start].decode("utf-8")
    file_data = payload[data_start:data_end]
    print("Filename:", filename)
    print("File Data:", file_data.decode("utf-8"))

    output_path = Path(__file__).parent / f"new-{filename}"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(file_data.decode("utf-8"))
        
    




print("Instructions: Input the name of the file (ex. Enter file to Decode>> WorldFile )")
print("     -Do note that if nothing is inputed, It will default to DataStorage_Save")

WORLD_PATH = Path(__file__).parent / input("Enter file to Decode>>")
if WORLD_PATH == "":
    WORLD_PATH = Path(__file__).parent / "DataStorage.txt"
getData()
decode()





"""
Unpack data:

Decode txt:     bytes(payload).decode("utf-8")

check if starts with --> EMRS
    If not: Stop

Check filename length
Save filename length to variable (FlnmLen)

Check content length    (4 bytes)
Save content length to variable (DatLen)


Read the next (FlnmLen) Characters
Save to variable (FileName)

Read the next (DatLen) Characters
Save to variable (FileData)

Create File with the name (FileName) and Data (FileData)
"""
