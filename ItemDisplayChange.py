import os

def change_unidentified(items):
	itemnumber = ""
	unidentifiedDisplayName = ""
	unidentifiedResourceName = ""
	unidentifiedDescriptionName = ""
	identifiedDisplayName = ""
	identifiedResourceName = ""
	identifiedDescriptionName = ""
	slotCount = "0"
	ClassNum = "0"
	costume = "false"
	try:
		itemnumber = items.split("]")[0].replace("[", "")
		unidentifiedDisplayName = items.split(", unidentifiedResourceName =")[0].split("unidentifiedDisplayName = ")[1].replace("\"", "")
		unidentifiedResourceName = items.split(", ")[1].split("= ")[1].replace("\"", "")
		unidentifiedDescriptionName = items.split("\"}, id")[0].split("unidentifiedDescriptionName = {\"")[1]
		identifiedDisplayName = items.split(", identifiedDisplayName = \"")[1].split("\", id")[0]
		identifiedResourceName = items.split(", identifiedResourceName = \"")[1].split("\", ")[0]
		identifiedDescriptionName = items.split("\nidentifiedDescriptionName = {\"")[1].split("\"}, ")[0]
		slotCount = items.split("slotCount = ")[1].split(", ")[0]
		ClassNum = items.split("ClassNum = ")[1].split(", ")[0]
		costume = items.split("costume = ")[1].split("}")[0]

	except:
		pass

	identification = unidentifiedDescriptionName.find("尚未鑑定")
	if identification == 0: # 如果unidentifiedDisplayName中有"尚未鑑定"4字,於此項加入洞數、【未鑑定】以及更改道具描述
		unidentifiedDescriptionName = identifiedDescriptionName
		if int(slotCount) > 0:
			slot_text = f"[{slotCount}]【未鑑定】"
		else:
			slot_text = "【未鑑定】"
		unidentifiedDisplayName = identifiedDisplayName + slot_text
		fix = True
	else: # 如果unidentifiedDisplayName中沒有"尚未鑑定"4字,只修改此項的名稱顯示洞數
		if int(slotCount) > 0:
			slot_text = f"[{slotCount}]"
			unidentifiedDisplayName = unidentifiedDisplayName + slot_text
			fix = True
		else: # 若unidentifiedDisplayName中沒有"尚未鑑定"4字且沒有洞數則完全不做修改
			fix = False

	return fix, itemnumber, unidentifiedDisplayName, unidentifiedResourceName, unidentifiedDescriptionName, identifiedDisplayName, identifiedResourceName, identifiedDescriptionName, slotCount, ClassNum, costume

def write_newfile(row): # mode = "a"可以繼續往下新增新值，不是每呼叫一次就用新值去覆蓋
	with open("iteminfo_new.lua", mode = "a", encoding = "ANSI") as outputfile:
		outputfile.write(row + "\n")

def openfile(file):
	with open(file, mode = "r", encoding = "ANSI") as openfile:
		opentext = openfile.read()

		return opentext



with open("iteminfo.lua", mode = "r", encoding = "ANSI") as file:
	aaa = file.read()

	beginning = aaa.split("\n[")[0]
	items_all = aaa.split("tbl = {\n")[1]
	items = items_all.split("}, \n")
	i = 1

	write_newfile(beginning) # 開頭寫入文章的處理

	for need_change in items:
		if i != len(items): # 如果物品資料並非最後一項則用以下方式處理
			fix, itemnumber, unidentifiedDisplayName, unidentifiedResourceName, unidentifiedDescriptionName, identifiedDisplayName, identifiedResourceName, identifiedDescriptionName, slotCount, ClassNum, costume = change_unidentified(need_change)

			print("fix =", fix)
			print("itemnumber =", itemnumber)
			print("unidentifiedDisplayName =", unidentifiedDisplayName)
			print("unidentifiedResourceName =", unidentifiedResourceName)
			print("unidentifiedDescriptionName =",unidentifiedDescriptionName)
			print("identifiedDisplayName =",identifiedDisplayName)
			print("identifiedResourceName =",identifiedResourceName)
			print("identifiedDescriptionName =",identifiedDescriptionName)
			print("slotCount =",slotCount)
			print("ClassNum =",ClassNum)
			print("costume =",costume)
			print("==========================================================")

			if fix == True: # 如果放進change_unidentified檢查出需要修改，則會透過下面規則修改
				write_unidentified = f"[{itemnumber}]" + " = {unidentifiedDisplayName = " + f"\"{unidentifiedDisplayName}\", unidentifiedResourceName = " + f"\"{unidentifiedResourceName}\", \nunidentifiedDescriptionName = " + "{\"" + f"{unidentifiedDescriptionName}" + "\"}, "

				if costume == "": # 先檢查是否為服飾
					write_identified = f"identifiedDisplayName = \"{identifiedDisplayName}\", identifiedResourceName = \"{identifiedResourceName}\", \nidentifiedDescriptionName = " + "{\"" + f"{identifiedDescriptionName}" + "\"}, " + f"slotCount = {slotCount}, ClassNum = {ClassNum}" + "}, \n"
				else:
					write_identified = f"identifiedDisplayName = \"{identifiedDisplayName}\", identifiedResourceName = \"{identifiedResourceName}\", \nidentifiedDescriptionName = " + "{\"" + f"{identifiedDescriptionName}" + "\"}, " + f"slotCount = {slotCount}, ClassNum = {ClassNum}, costume = {costume}" + "}, "

				write_text = write_unidentified + write_identified
				write_newfile(write_text)
			else: # 如果放進change_unidentified檢查出都不需修改，則會透過下面規則修改
				write_text = need_change + "}, "
				write_newfile(write_text)

			i += 1 # 計數用(檔案內的資料筆數)

		else: # 如果是最後一項資料則修改需要特別處理
			last_text = need_change.split("}}")[0]
			fix, itemnumber, unidentifiedDisplayName, unidentifiedResourceName, unidentifiedDescriptionName, identifiedDisplayName, identifiedResourceName, identifiedDescriptionName, slotCount, ClassNum, costume = change_unidentified(last_text)

			print("fix =", fix)
			print("itemnumber =", itemnumber)
			print("unidentifiedDisplayName =", unidentifiedDisplayName)
			print("unidentifiedResourceName =", unidentifiedResourceName)
			print("unidentifiedDescriptionName =",unidentifiedDescriptionName)
			print("identifiedDisplayName =",identifiedDisplayName)
			print("identifiedResourceName =",identifiedResourceName)
			print("identifiedDescriptionName =",identifiedDescriptionName)
			print("slotCount =",slotCount)
			print("ClassNum =",ClassNum)
			print("costume =",costume)

			if fix == True: # 如果放進change_unidentified檢查出需要修改，則會透過下面規則修改
				write_unidentified = f"[{itemnumber}]" + " = {unidentifiedDisplayName = " + f"\"{unidentifiedDisplayName}\", unidentifiedResourceName = " + f"\"{unidentifiedResourceName}\", \nunidentifiedDescriptionName = " + "{\"" + f"{unidentifiedDescriptionName}" + "\"}, "

				if costume == "": # 先檢查是否為服飾
					write_identified = f"identifiedDisplayName = \"{identifiedDisplayName}\", identifiedResourceName = \"{identifiedResourceName}\", \nidentifiedDescriptionName = " + "{\"" + f"{identifiedDescriptionName}" + "\"}, " + f"slotCount = {slotCount}, ClassNum = {ClassNum}" + "}, \n"
				else:
					write_identified = f"identifiedDisplayName = \"{identifiedDisplayName}\", identifiedResourceName = \"{identifiedResourceName}\", \nidentifiedDescriptionName = " + "{\"" + f"{identifiedDescriptionName}" + "\"}, " + f"slotCount = {slotCount}, ClassNum = {ClassNum}, costume = {costume}" + "},\n}"

				write_text = write_unidentified + write_identified
				write_newfile(write_text)
			else: # 如果放進change_unidentified檢查出都不需修改，則會透過下面規則修改
				write_text = last_text + "},\n}"
				write_newfile(write_text)

			endtext = openfile("end_text.txt") # 最後面需要額外寫入的文章
			write_newfile(endtext)

# 刪除舊iteminfo.lua檔案
try:
	os.remove("iteminfo.lua")
except OSError as e:
	print(e)
else:
	print("iteminfo.lua is deleted successfully")

# 將iteminfo_new.lua改名為iteminfo.lua
os.rename("iteminfo_new.lua", "iteminfo.lua")
print("file name ieminfo_new.lua is changed to iteminfo.lua successfully")