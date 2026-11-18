import struct
from pathlib import Path
import shutil
import anvil

# A short marker at the start of our payload lets unpack() recognize data
# created by this program instead of interpreting arbitrary image bytes.
MAGIC = b"WSTR"
# Sets the location of the template world 
WorldTemplate = Path(__file__).parent / "DataStorageTemplate"
#copy template world
COPY = WorldTemplate.with_name("DataStorage_Save")
#define regions dictionary to store region objects
regions = {}

file_to_encode = Path(__file__).parent / "DataStorage.txt"

EncodedBlocks = ["air","red_stained_glass", "orange_stained_glass", "yellow_stained_glass","lime_stained_glass","green_stained_glass","cyan_stained_glass","light_blue_stained_glass","purple_stained_glass","pink_stained_glass"]
OnesData = []
TensData = []
HundredsData = []



#  --------------------------
#    Data Storage Functions
#  --------------------------

def pack(path: Path) -> bytes:
    # Read the complete source file without decoding it as text. This works
    # for binary formats such as images, archives, and executables too.
    data = path.read_bytes()

    # Store only the input's filename, not its folder path. UTF-8 turns the
    # filename into bytes so it can be placed in the binary header.
    name = path.name.encode()

    # Header layout: 4-byte marker, 1-byte filename length, 4-byte data
    # length, then the filename bytes. > means big-endian; B is an unsigned
    # byte; I is an unsigned 4-byte integer.
    header = MAGIC + struct.pack(">BI", len(name), len(data)) + name

    # The unpacked file contents come immediately after the header.
    return header + data


def copy_world():
    if not COPY.exists():
        shutil.copytree(WorldTemplate, COPY)

def block(x, y, z, block_name):
    # Make sure the copied world exists before editing it.
    copy_world()

    # Each region covers 256 blocks along the X and Z axes.
    region_x = x // 256
    region_z = z // 256

    # Reuse the region so earlier block placements are kept.
    if (region_x, region_z) not in regions:
        regions[(region_x, region_z)] = anvil.EmptyRegion(region_x, region_z)

    # Place the block at the given world coordinates.
    regions[(region_x, region_z)].set_block(anvil.Block("minecraft", block_name), x, y, z)
    print(f"Placing block {block_name} at ({x}, {y}, {z})")


def splitTheData(data: bytes):
    for byte in data:
        hundreds = byte // 100
        tens = (byte // 10) % 10
        ones = byte % 10
        HundredsData.append(hundreds)
        TensData.append(tens)
        OnesData.append(ones)

def export():
    for i in range(len(HundredsData)):
        block(i % 256, 2, i // 256, EncodedBlocks[HundredsData[i]])
    for i in range(len(TensData)):
        block(i % 256, 1, i // 256, EncodedBlocks[TensData[i]])
    for i in range(len(OnesData)):
        block(i % 256, 0, i // 256, EncodedBlocks[OnesData[i]])

print("Instructions:")
print()
print("     1. Choose file to encode and put it in the same folder as this pyton file.")
print("     2. Run the code using either the dubble clicking run.ssh, or by using the standard python command.")
print("     3. Input the name of the file (ex. Enter file to encode>> cat.jpg )")
file_to_encode = input("Enter file to encode>>")

payload = pack(Path(__file__).parent / file_to_encode)
splitTheData(payload)
export()


for (region_x, region_z), region in regions.items():
    region_file = COPY / "dimensions" / "minecraft" / "overworld" / "region" / f"r.{region_x}.{region_z}.mca"
    region_file.parent.mkdir(parents=True, exist_ok=True)
    region.save(str(region_file))

#testing