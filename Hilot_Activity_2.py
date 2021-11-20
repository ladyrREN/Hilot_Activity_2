from queue import Queue, PriorityQueue
import pygame as py

WINDOW_WIDTH = 1202
WINDOW_HEIGHT = 685

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
light_green = (104, 255, 104)
red_light = (2, 7, 163)
screen_fill = (240, 108, 108)

class Grid:

    def __init__(self, rows, cols, window=None, width=None, height=None):
        self.rows = rows
        self.cols = cols
        self.window = window
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cubes(i, j) for j in range(cols)] for i in range(rows)]
        self.x = 0
        self.y = 0
        if self.width is not None:
            self.dif = self.width // cols

        count = 0
        for i in range(rows):
            for j in range(cols):
                self.cubes[i][j].make_values(count)
                count += 1

        for i in range(rows):
            for j in range(cols):
                if (rows - 1) > i > 0 and 0 < j < (cols - 1):
                    self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], right=self.cubes[i][j + 1],
                                                      up=self.cubes[i - 1][j], down=self.cubes[i + 1][j])

                elif i == 0:
                    if j == 0:
                        self.cubes[i][j].make_connections(right=self.cubes[i][j + 1], down=self.cubes[i + 1][j])
                    elif j == cols - 1:
                        self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], down=self.cubes[i + 1][j])
                    else:
                        self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], right=self.cubes[i][j + 1],
                                                          down=self.cubes[i + 1][j])
                elif i == (rows - 1):
                    if j == 0:
                        self.cubes[i][j].make_connections(right=self.cubes[i][j + 1], up=self.cubes[i - 1][j])
                    elif j == cols - 1:
                        self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], up=self.cubes[i - 1][j])
                    else:
                        self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], right=self.cubes[i][j + 1],
                                                          up=self.cubes[i - 1][j])

                else:
                    if j == 0:
                        self.cubes[i][j].make_connections(right=self.cubes[i][j + 1], up=self.cubes[i - 1][j],
                                                          down=self.cubes[i + 1][j])
                    else:
                        self.cubes[i][j].make_connections(left=self.cubes[i][j - 1], up=self.cubes[i - 1][j],
                                                          down=self.cubes[i + 1][j])

    def get_cord(self, pos):

        click_x = pos[0] // self.dif

        click_y = pos[1] // self.dif
        return (click_x, click_y)

    def draw(self):
        self.window.fill((133, 41, 153))
        for i in range((self.rows + 1)):
            py.draw.line(self.window, (0,0,0), (self.x, i * self.dif), (self.width, i * self.dif), 1)
            py.draw.line(self.window, (0,0,0), (i * self.dif, self.y), (i * self.dif, self.height), 1)

    def select_start(self, row, col):
        py.draw.rect(self.window, (255, 0, 0), (row * self.dif, col * self.dif, self.dif, self.dif))

    def select_end(self, row, col):
        py.draw.rect(self.window, (255, 153, 153), (row * self.dif, col * self.dif, self.dif, self.dif))

    def get_cubes(self):
        return self.cubes

    def add_blocks(self, row, col):
        self.cubes[row][col].block_cell()

    def remove_blocks(self, row, col):
        self.cubes[row][col].unblock_cell()


class Cubes:

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.value = None
        self.blocked = False

    def make_values(self, value):
        self.value = value

    def make_connections(self, left=None, right=None, up=None, down=None):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def value(self):
        return self.value

    def print_row_col(self):
        return self.row, self.column

    def show_connections(self):
        return [self.left, self.right, self.up, self.down]

    def block_cell(self):
        self.blocked = True

    def unblock_cell(self):
        self.blocked = False

    def get_cell_condition(self):
        return self.blocked


def button(msg, x, y, w, h, ic, ac, action=None, parameters=None):
    mouse = py.mouse.get_pos()
    click = py.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        py.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameters:
                action(parameters)
            else:
                action()

    else:
        py.draw.rect(screen, ic, (x, y, w, h))

    smallText = smallfont.render(msg, True, black)
    textRect = smallText.get_rect()
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(smallText, textRect)


def intro():
    while True:
        for event in py.event.get(a_star_loop()):
            if event.type == py.QUIT:
                py.quit()
                quit()

        py.display.update()


def d(current, neighbor):
    x1, y1 = current.print_row_col()
    x2, y2 = current.print_row_col()
    return abs(x2 - x1) + abs(y2 - y1)


def heuristic(node, e):
    x1, y1 = node.print_row_col()
    x2, y2 = e.print_row_col()
    return abs(x2 - x1) + abs(y2 - y1)


def a_star(s, e, rows, cols):
    openSet = PriorityQueue()

    openSet.put((heuristic(s, e), 0, s))
    parentMap = {}
    visited = [False for i in range(rows * cols)]
    gScore = {i: float('inf') for i in range(rows * cols)}
    gScore[s.value] = 0
    traversal = []
    fScore = {i: float('inf') for i in range(rows * cols)}
    fScore[s.value] = 0

    count = 100
    while not openSet.empty():
        current = openSet.get()

        if current[2] == e:
            break

        for neighbor in current[2].show_connections():
            if neighbor and not neighbor.get_cell_condition():
                tentative_gScore = gScore[current[2].value] + d(current[2], neighbor)
                traversal.append(neighbor)

                if tentative_gScore < gScore[neighbor.value]:
                    count -= 1
                    parentMap[neighbor] = current[2]
                    gScore[neighbor.value] = tentative_gScore
                    fScore[neighbor.value] = gScore[neighbor.value] + heuristic(neighbor, e)
                    openSet.put((fScore[neighbor.value], count, neighbor))

                    visited[neighbor.value] = True
    return parentMap, traversal

def a_star_loop():
    gridSurface = py.Surface((601, 600))
    state = True
    rows = 10
    cols = 10
    grid = Grid(rows, cols, gridSurface, 601, 600)
    clicked = None
    run = True
    once = True
    complete_first_time = False
    end = False
    start = False
    find = False
    starting_position = None
    end_position = None
    cubes_ = grid.get_cubes()
    make_wall = False
    del_wall = False
    blocks = {}
    diff = WINDOW_WIDTH // 20

    while run:

        grid.draw()
        screen.fill(screen_fill)

        button("Start position", 1000, 50, 135, 50, red, red_light)
        button("End position", 1000, 120, 130, 50, red, red_light)
        button("Add blocks", 1000, 270, 110, 50, red, red_light)
        button("Remove blocks", 1000, 350, 140, 50, red, red_light)

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()
                clicked = grid.get_cord(pos)

        if state:
            if clicked:

                if (1000 + 135) > pos[0] > 1000 and (50 + 50) > pos[1] > 50:
                    start = True

                if (1000 + 130) > pos[0] > 1000 and (120 + 50) > pos[1] > 120:
                    start = False
                    end = True
                if end_position and starting_position:
                    if not once:
                        if (1000 + 200) > pos[0] > 1000 and (190 + 50) > pos[1] > 190:
                            find = True
                            end = False
                if (1000 + 110) > pos[0] > 1000 and (270 + 50) > pos[1] > 270:
                    start = False
                    end = False
                    find = False
                    make_wall = True
                if (1000 + 140) > pos[0] > 1000 and (350 + 50) > pos[1] > 350:
                    start = False
                    end = False
                    find = False
                    make_wall = False
                    del_wall = True

            if start:
                if blocks:
                    for i in blocks.values():
                        py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))

                grid.select_start(clicked[0], clicked[1])
                starting_position = clicked
                screen.blit(gridSurface, (0, 0))
                py.display.update()

            elif end:
                if blocks:
                    for i in blocks.values():
                        py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))

                grid.select_end(clicked[0], clicked[1])
                end_position = clicked
                if starting_position:
                    grid.select_start(starting_position[0], starting_position[1])

                button("Find path", 1000, 190, 200, 59, red, red_light)
                screen.blit(gridSurface, (0, 0))
                py.display.update()
            elif find:
                if blocks:
                    for i in blocks.values():
                        py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))

                if (starting_position[0] < 50 and starting_position[1] < 50) and (
                        end_position[0] < 50 and end_position[1] < 50):
                    grid.select_start(starting_position[0], starting_position[1])

                    path, traversal = a_star(cubes_[int(starting_position[0])][int(starting_position[1])],
                                             cubes_[int(end_position[0])][int(end_position[1])], rows, cols)
                    for i in traversal:
                        bo = py.draw.rect(screen, (240, 108, 108),
                                          (i.print_row_col()[0] * diff, i.print_row_col()[1] * diff, diff, diff), 1)
                        py.time.delay(5)
                        py.display.update(bo)

                    curr = cubes_[int(end_position[0])][int(end_position[1])]
                    curr = path[curr]
                    grid.select_end(curr.print_row_col()[0], curr.print_row_col()[1])

                    while curr != cubes_[int(starting_position[0])][int(starting_position[1])]:

                        bo = py.draw.rect(gridSurface, (255, 0, 0),
                                          (curr.print_row_col()[0] * diff, curr.print_row_col()[1] * diff, diff, diff),
                                          1)
                        if not complete_first_time:
                            screen.blit(gridSurface, (0, 0))
                            py.display.update(bo)
                            py.time.delay(3)

                        curr = path[curr]
                    state = False

                    if not complete_first_time:
                        complete_first_time = True

                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                else:
                    if (starting_position[0] > 50 or starting_position[1] > 50):
                        button("Please Select a Starting Position!", 602, 10, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                    elif (end_position[0] > 50 or end_position[1] > 50):
                        button("Please select an End Position!", 602, 0, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
                    else:
                        button("Please select both Positions!", 602, 0, 400, 50, red, red)
                        screen.blit(gridSurface, (0, 0))
                        py.display.update()
            elif make_wall:
                if (clicked[0] < 10 and clicked[1] < 10):
                    bo = py.draw.rect(gridSurface, (0, 0, 0), (clicked[0] * diff, clicked[1] * diff, diff, diff))
                    blocks[cubes_[clicked[0]][clicked[1]].value] = clicked
                    grid.add_blocks(clicked[0], clicked[1])
                    screen.blit(gridSurface, (0, 0))
                    py.display.update(bo)
            elif del_wall:
                if (clicked[0] < 50 and clicked[1] < 50):
                    if blocks:
                        try:
                            del blocks[cubes_[clicked[0]][clicked[1]].value]
                            grid.remove_blocks(clicked[0], clicked[1])
                            for i in blocks.values():
                                py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))
                            if starting_position and end_position:
                                button("Find path", 1000, 190, 200, 59, red, red_light)
                                grid.select_start(starting_position[0], starting_position[1])
                                grid.select_end(end_position[0], end_position[1])
                            screen.blit(gridSurface, (0, 0))
                            py.display.update()
                        except Exception:
                            pass

        else:
            if blocks:
                for i in blocks.values():
                    py.draw.rect(gridSurface, (0, 0, 0), (i[0] * diff, i[1] * diff, diff, diff))

            grid.select_start(starting_position[0], starting_position[1])

            curr = cubes_[int(end_position[0])][int(end_position[1])]
            grid.select_end(curr.print_row_col()[0], curr.print_row_col()[1])
            curr = path[curr]

            while curr != cubes_[int(starting_position[0])][int(starting_position[1])]:
                py.draw.rect(gridSurface, (255, 0, 100),
                             (curr.print_row_col()[0] * diff, curr.print_row_col()[1] * diff, diff, diff), 1)

                curr = path[curr]

            button("Refresh", 500, 610, 200, 59, red, red_light, a_star_loop)

            screen.blit(gridSurface, (0, 0))
            py.display.update()

        if once:
            once = False
            screen.blit(gridSurface, (0, 0))
            py.display.update()

        clock.tick(60)
    py.quit()
    quit()


if __name__ == "__main__":
    py.init()
    key = None
    py.display.set_caption("Hilot_A*")
    myfont = py.font.SysFont('Calibri', 30)
    smallfont = py.font.SysFont('Calibri', 20)
    screen = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = py.time.Clock()
    intro()