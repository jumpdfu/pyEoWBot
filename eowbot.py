import pymem.memory
import keyboard
import json

# ************* Блок глобальных переменных *************************

max_hpAddr = 0x0057B3A4  # Максимальное значение здоровья персонажа
cur_hpAddr = 0x0057B39C  # Текущее значение здоровья персонажа
staminaAddr = 0x00553AD8  # Текущее значение бодрости персонажа
cur_exp_Addr = 0x0057B3B0  # Текущее значение опыта персонажа
cur_xAddr = 0x00581984  # Текущее значение горизонтальной Х координаты персонажа
cur_yAddr = 0x00581988  # Текущее значение вертикальной У координаты персонажа
cur_mapAddr = 0x0052C138  # Номер карты на которой находится персонаж
target_xAddr = 0x01369158  # Текущее значение горизонтальной Х координаты в которую должен идти персонаж
target_yAddr = 0x0136915C  # Текущее значение вертикальной У координаты в которую должен идти персонаж
movementAddr = 0x01369155  # Адрес признака движения персонажа. 0 - стоит, 1 идет
map_top_leftAddr = 0x0058199C  # Адрес левой верхней точки карты, начало двумерного вертикального массива. Каждая
# следующая точка на карте вычисляется смещением в 192 байта
map_top_leftObjectDirectionAddr = map_top_leftAddr + 4  # Направление в котором смотрит объект(если такой есть) из левой
# верхней точки карты
map_top_leftObjectHPAddr = map_top_leftAddr + 40
magic_target_idAddr = 0x0052C12C  # Адрес ID монстра или персонажа выделенного через ctrl+лкм


# ************* Конец Блока глобальных переменных *************************


def game_connect(process_name="MUDClient.exe"):
    mem = pymem.memory
    hWnd = pymem.Pymem(process_name)
    memProcess = hWnd.process_handle
    process = mem, memProcess
    return process


def scan_map(search=None):
    mem, memProcess = game_connect()
    found_id = list()

    X, Y = -10, -10
    mat = map_top_leftAddr
    direction = mem.read_int(memProcess, map_top_leftObjectDirectionAddr)
    objHP = mem.read_int(memProcess, map_top_leftObjectHPAddr)

    matrix = ([[mat, mem.read_int(memProcess, mat), mem.read_int(memProcess, cur_xAddr) - 10,
                mem.read_int(memProcess, cur_yAddr) - 10, direction, objHP]])

    for i in range(440):
        mat += 192
        Y += 1
        if i % 21 == 0 and i != 0:
            X += 1
            Y = -10

        objHP = mem.read_int(memProcess, mat + 4)
        # Направление в котором смотрит персонаж.
        direction = mem.read_int(memProcess, mat + 40)
        isee_id = mem.read_int(memProcess, mat)
        if isee_id == 0:
            direction = None
        isee_id_coordX = mem.read_int(memProcess, cur_xAddr) + X
        isee_id_coordY = mem.read_int(memProcess, cur_yAddr) + Y

        tmp_list = [mat, isee_id, isee_id_coordX, isee_id_coordY, direction, objHP]
        if search is not None and search == mem.read_int(memProcess, mat):
            found_id = tmp_list
        matrix.append(tmp_list)
    if search is not None:
        return found_id
    else:
        return matrix


def track_rec(file_path='json_data.json'):
    mem, memProcess = game_connect()
    workie: bool = True
    pause: bool = False
    oldX = 0
    oldY = 0
    coords = []
    while workie:
        if keyboard.is_pressed('alt+F12'):
            with open(file_path, 'w') as outfile:
                print("Recording stopped")
                json.dump(coords, outfile, indent=2)
            workie = False
        if keyboard.is_pressed('alt+F11'):
            print("Recording paused")
            pause = True

        if pause:
            while pause:
                if keyboard.is_pressed('alt+F10'):
                    print("Recording unpause")
                    pause = False

        X = mem.read_int(memProcess, cur_xAddr)
        Y = mem.read_int(memProcess, cur_yAddr)
        if oldX != X or oldY != Y:
            oldX = X
            oldY = Y
            coords.append([X, Y])
            print("Recording " + str(X) + " : " + str(Y))


def track_go(file_path='json_data.json'):
    mem, memProcess = game_connect()
    workie: bool = True
    pause: bool = False
    oldX = 0
    oldY = 0
    with open(file_path, 'r') as infile:
        coords = json.load(infile)
        while workie:
            if keyboard.is_pressed('alt+F12'):
                workie = False
            if keyboard.is_pressed('alt+F11'):
                pause = True
            if pause:
                while pause:
                    if keyboard.is_pressed('alt+F10'):
                        pause = False
            # Цикл присвоения
            for coord in coords:
                targetX, targetY = coord

                move = False
                while not move:
                    curX = mem.read_int(memProcess, cur_xAddr)
                    curY = mem.read_int(memProcess, cur_yAddr)
                    if abs(targetX - curX) > 3 or abs(targetY - curY) > 3:
                        mem.write_int(memProcess, target_xAddr, oldX)
                        mem.write_int(memProcess, target_yAddr, oldY)
                        mem.write_bool(memProcess, movementAddr, True)
                    else:
                        move = True

                mem.write_int(memProcess, target_xAddr, targetX)
                mem.write_int(memProcess, target_yAddr, targetY)
                mem.write_bool(memProcess, movementAddr, True)
                # time.sleep(0.4)
                oldX, oldY = coord
                print("Going to " + str(targetX) + ":" + str(targetY))
            workie = False
            print("Track Finish riches")


def follow_target(target_id: int = None):
    mem, memProcess = game_connect()
    if target_id is None:
        target_id = mem.read_int(memProcess, magic_target_idAddr)
    workie: bool = True
    pause: bool = False
    oldX = 0
    oldY = 0
    while workie:
        if keyboard.is_pressed('alt+F12'):
            workie = False
        if keyboard.is_pressed('alt+F11'):
            pause = True
        if pause:
            while pause:
                if keyboard.is_pressed('alt+F10'):
                    pause = False

        target = scan_map(target_id)
        targetAddr, targetID, targetX, targetY, direction, objHP = target
        move = False
        while not move:
            curX = mem.read_int(memProcess, cur_xAddr)
            curY = mem.read_int(memProcess, cur_yAddr)
            if abs(targetX - curX) > 3 or abs(targetY - curY) > 3 and oldX != 0 and oldY != 0:
                mem.write_int(memProcess, target_xAddr, oldX)
                mem.write_int(memProcess, target_yAddr, oldY)
                mem.write_bool(memProcess, movementAddr, True)
            else:
                move = True

        mem.write_int(memProcess, target_xAddr, targetX)
        mem.write_int(memProcess, target_yAddr, targetY)
        mem.write_bool(memProcess, movementAddr, True)
        # time.sleep(0.4)
        oldX, oldY = targetX, targetY
        print("Going to " + str(targetX) + ":" + str(targetY))