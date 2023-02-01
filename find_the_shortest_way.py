import math


class MyQueue:
    def __init__(self):
        self.my_queue = list()

    def app_end(self, obj):
        self.my_queue.append(obj)

    def app_front(self, obj):
        self.my_queue.insert(0, obj)

    def pop_end(self):
        if self.my_queue:
            return self.my_queue.pop()

    def pop_front(self):
        if self.my_queue:
            return self.my_queue.pop(0)

    def __bool__(self):
        return bool(self.my_queue)


class Vertex:
    def __init__(self):
        self._links = list()  # contains Link objects
        self.price = math.inf

    def get_links(self):
        return self._links

    def add_link(self, link):
        self._links.append(link)

    links = property()
    links = links.getter(get_links)
    links = links.setter(add_link)


class Link:

    def __init__(self, v1, v2, dist=1):
        self._v1 = v1
        self._v2 = v2
        self._dist = dist

    @property
    def v1(self):
        return self._v1

    def get_v2(self):
        return self._v2

    v2 = property(get_v2)

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        self._dist = value


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []

    def add_vertex(self, v):
        if v not in self._vertex:
            self._vertex.append(v)

    def add_link(self, link):
        if len(
                list(
                    filter(
                        lambda x: link.v1 in (x.v1, x.v2) and link.v2 in (x.v1, x.v2), self._links
                    )
                )
        ) == 0:
            self._links.append(link)
            link.v1.links = link
            link.v2.links.append(link)
        if link.v1 not in self._vertex:
            self._vertex.append(link.v1)
        if link.v2 not in self._vertex:
            self._vertex.append(link.v2)

    def find_path_by_dijkstra(self, srart_v: Vertex, stop_v: Vertex):
        def burning(vertex: Vertex):
            for link in vertex.links:
                other_vertex = link.v1 if link.v1 != vertex else link.v2
                tmp_price = link.dist + vertex.price
                if tmp_price < other_vertex.price:
                    other_vertex.price = tmp_price
                    queue.app_end(other_vertex)

        def reconstruct_way(stop_v: Vertex, srart_v: Vertex):
            vertexes = []
            links = []
            PATHS = []
            current_vertex = stop_v

            def recurtion_method(current_vertex: Vertex):
                vertexes.append(current_vertex)
                if current_vertex == srart_v:
                    PATHS.append({tuple(vertexes.copy()): tuple(links.copy())})
                    vertexes.clear()
                    links.clear()
                    return
                else:
                    for link in current_vertex.links:
                        next_vertex = link.v1 if link.v1 != current_vertex else link.v2
                        if current_vertex.price - link.dist == next_vertex.price:
                            links.append(link)
                            recurtion_method(next_vertex)

            recurtion_method(current_vertex)
            return PATHS

        queue = MyQueue()
        srart_v.price = 0
        queue.app_end(srart_v)
        while queue:
            current_vertex = queue.pop_front()
            burning(current_vertex)  # check vertex's price and add vertex to queue if price has been updated

        return reconstruct_way(stop_v, srart_v)

    def find_path_by_recurtion(self, srart_v: Vertex, stop_v: Vertex):
        PATHS = {}
        vertexes = ()
        links = ()

        def recurtion(current_vertex, vertexes, links):
            vertexes += current_vertex,
            if current_vertex == srart_v:
                PATHS[vertexes] = links
            else:
                for link in current_vertex.links:
                    if link not in links:
                        tmp_current_vertex = link.v1 if link.v1 != current_vertex else link.v2
                        if tmp_current_vertex not in vertexes:
                            recurtion(tmp_current_vertex, vertexes, links + (link,))

        recurtion(stop_v, vertexes, links)
        return PATHS

    def find_path_alt(self, start_v, stop_v):
        paths_dict = self.find_path_by_dijkstra(start_v, stop_v)[0]
        my_vertexes = list(list(paths_dict.keys())[0][::-1])
        my_links = list(list(paths_dict.values())[0][::-1])
        return my_vertexes, my_links

    def find_path(self, start_v, stop_v):
        PATHS = self.find_path_by_recurtion(start_v, stop_v)
        SORTED_PATHS = sorted(
            PATHS, key=lambda x: sum(
                y.dist for y in PATHS[x]
            )
        )
        tmp_path = SORTED_PATHS[0]
        right_vertexes = tmp_path[::-1]
        right_links = PATHS[tmp_path][::-1]
        return list(right_vertexes), right_links


class Station(Vertex):
    def __init__(self, name, *args, **kwargs):
        super(Station, self).__init__(*args, **kwargs)
        self.name = name

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return self.__repr__()


class LinkMetro(Link):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


map_metro = LinkedGraph()
v1 = Station("Сретенский бульвар")
v2 = Station("Тургеневская")
v3 = Station("Чистые пруды")
v4 = Station("Лубянка")
v5 = Station("Кузнецкий мост")
v6 = Station("Китай-город 1")
v7 = Station("Китай-город 2")

map_metro.add_link(LinkMetro(v1, v2, 1))
map_metro.add_link(LinkMetro(v2, v3, 1))
map_metro.add_link(LinkMetro(v1, v3, 1))

map_metro.add_link(LinkMetro(v4, v5, 1))
map_metro.add_link(LinkMetro(v6, v7, 1))

map_metro.add_link(LinkMetro(v2, v7, 5))
map_metro.add_link(LinkMetro(v3, v4, 3))
map_metro.add_link(LinkMetro(v5, v6, 3))

print(len(map_metro._links))
print(len(map_metro._vertex))
path = map_metro.find_path_alt(v1, v6)  # от сретенского бульвара до китай-город 1
print(path[0])    # [Сретенский бульвар, Тургеневская, Китай-город 2, Китай-город 1]
print(sum([x.dist for x in path[1]]))  # 7