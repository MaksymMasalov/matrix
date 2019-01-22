import random
from typing import Tuple, List


class Node:
    def __init__(self, position: Tuple[int, int], infected: bool):
        self.position = position
        if infected:
            self.infected_at = 0
        else:
            self.infected_at = None

    def infect(self, infected_at):
        if self.infected_at is None or self.infected_at > infected_at:
            self.infected_at = infected_at
            return True
        return False

    @property
    def infected(self):
        return self.infected_at is not None

    def __str__(self):
        infected = 'Infected' if self.infected else 'Not infected'
        return '{}, position={}'.format(infected, self.position)

    def __hash__(self):
        return hash(self.position)


class Net:
    def __init__(self, matrix: List[List[Node]]):
        self.matrix = matrix

        self._unchecked_nodes = None
        self._max_infected_at = 0

        self._index_change_cache = None

    def infect(self):
        while self._unchecked_nodes is None or self._unchecked_nodes:
            self._infect()
            self.print_matrix()
        return self._max_infected_at

    def print_matrix(self):
        print(' ', end='')
        print('_' * (len(self.matrix[0]) * 2 + 1))
        for row in self.matrix:
            for node in row:
                print('|', end='')
                if node is None:
                    print('O', end='')
                elif node.infected:
                    print('I'.format(node.infected_at), end='')
                else:
                    print('A', end='')
            print('|')

        print('-' * (len(self.matrix[0]) * 2 + 1))

    def _infect(self):
        new_unchecked_nodes = set()
        if self._unchecked_nodes is None:
            nodes = self._get_all_nodes()
        else:
            nodes = self._unchecked_nodes

        for node in nodes:
            if node.infected:
                if node in new_unchecked_nodes:
                    continue
                new_unchecked_nodes.update(self._infect_neighbours(node))

        self._unchecked_nodes = new_unchecked_nodes

    def _get_all_nodes(self):
        for row in self.matrix:
            for node in row:
                if node is None:
                    continue
                yield node

    def _infect_neighbours(self, node):
        infected_at = node.infected_at + 1
        for index_change in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            i = node.position[0] + index_change[0]
            j = node.position[1] + index_change[1]
            try:
                infecting_node = self.matrix[i][j]
            except IndexError:
                continue

            if infecting_node is None:
                continue

            infected = infecting_node.infect(infected_at)
            if infected:
                self._max_infected_at = max((self._max_infected_at, infected_at))
                yield infecting_node


def main():
    N, M = 5, 5

    matrix = []
    for i in range(N):
        row = []
        for j in range(M):
            condition = random.randint(0, 100)
            if 0 <= condition < 10:
                # off
                row.append(None)
            elif 10 <= condition < 90:
                # on
                row.append(Node(position=(i, j), infected=False))
            else:
                # infected
                row.append(Node(position=(i, j), infected=True))

        matrix.append(row)

    net = Net(matrix)
    net.print_matrix()
    seconds = net.infect()
    print('Matrix would be infected in {} seconds'.format(seconds))


main()
