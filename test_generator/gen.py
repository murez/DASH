import copy

# with open("/public/home/qinfr/index_nvidia_GTX_1080.txt") as f:
#     lines = f.readlines()
#     old_arg1 = ""
#     last1_line = []
#     last2_line = []
#     for line in lines:
#         # print(line)
#         args = line.strip().split(",")
#         if args[0] != old_arg1 and last2_line!= []:
#             print(last2_line[0], last2_line[1],"NVIDIAGeForceGTX1080")
#             print(last1_line[0], last1_line[1],"NVIDIAGeForceGTX1080")
#             old_arg1 = args[0]
#         last2_line = copy.deepcopy(last1_line)
#         last1_line = copy.deepcopy(args)
#     print(last2_line[0], last2_line[1],"NVIDIAGeForceGTX1080")
#     print(last1_line[0], last1_line[1],"NVIDIAGeForceGTX1080")

# with open("/public/home/qinfr/index_nvidia_RTX_2080.txt") as f:
#     lines = f.readlines()
#     old_arg1 = ""
#     last1_line = []
#     last2_line = []
#     for line in lines:
#         # print(line)
#         args = line.strip().split(",")
#         if args[0] != old_arg1 and last2_line!= []:
#             print(last2_line[0], last2_line[1],"NVIDIAGeForceRTX2080Ti")
#             print(last1_line[0], last1_line[1],"NVIDIAGeForceRTX2080Ti")
#             old_arg1 = args[0]
#         last2_line = copy.deepcopy(last1_line)
#         last1_line = copy.deepcopy(args)
#     print(last2_line[0], last2_line[1],"NVIDIAGeForceRTX2080Ti")
#     print(last1_line[0], last1_line[1],"NVIDIAGeForceRTX2080Ti")

with open("/public/home/qinfr/index_nvidia_TITAN_XP.txt") as f:
    lines = f.readlines()
    old_arg1 = ""
    last1_line = []
    last2_line = []
    for line in lines:
        # print(line)
        args = line.strip().split(",")
        if args[0] != old_arg1 and last2_line!= []:
            print(last2_line[0], last2_line[1],"NVIDIATITANRTX")
            print(last1_line[0], last1_line[1],"NVIDIATITANRTX")
            old_arg1 = args[0]
        last2_line = copy.deepcopy(last1_line)
        last1_line = copy.deepcopy(args)
    print(last2_line[0], last2_line[1],"NVIDIATITANRTX")
    print(last1_line[0], last1_line[1],"NVIDIATITANRTX")