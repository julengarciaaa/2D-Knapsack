import portion as P
from collections import defaultdict

class LayerState:
    __slots__ = ['layer', 'warehouse', 'p_points', 'vertical_edges', 'horizontal_edges', '_cached_hash']

    def __init__(self, layer, warehouse, p_points=None, vertical_edges=None, horizontal_edges=None):
        self.layer = layer
        self.warehouse = warehouse
        
        # Store as tuple to ensure immutability
        self.p_points = tuple(p_points) if p_points is not None else ((0, 0),)

        # Initialize or copy edge dictionaries
        if vertical_edges is None:
            self.vertical_edges = defaultdict(lambda: P.empty())
            self.vertical_edges[0] = P.closedopen(0, layer.get_width())
            self.vertical_edges[layer.get_length()] = P.closedopen(0, layer.get_width())
        else:
            self.vertical_edges = vertical_edges

        if horizontal_edges is None:
            self.horizontal_edges = defaultdict(lambda: P.empty())
            self.horizontal_edges[0] = P.closedopen(0, layer.get_length())
            self.horizontal_edges[layer.get_width()] = P.closedopen(0, layer.get_length())
        else:
            self.horizontal_edges = horizontal_edges
        
        # Cache the hash because the state never changes
        self._cached_hash = hash(frozenset(self.layer.get_placements()))

    def get_layer(self):
        return self.layer
    
    def get_warehouse(self):
        return self.warehouse
    
    def get_p_points(self):
        return self.p_points

    # Commits a placement and calculates the new placing points.
    def commit_placement(self, placement):
        x, y = placement.get_p_point()
        p_l, p_w = placement.get_length(), placement.get_width()

        # Update edges (creating fresh copies for the new state)
        new_v_edges = self.vertical_edges.copy()
        new_h_edges = self.horizontal_edges.copy()

        # Calculate the new placing points
        active_points = [p for p in self.p_points if p != (x, y)]
        
        p1, p2 = (x, y + p_w), (x + p_l, y)
        # Check the existance of supports
        p1_has_v_support = p1[1] in new_v_edges[p1[0]]
        p2_has_v_support = p2[1] in new_v_edges[p2[0]]
        p1_has_h_support = p1[0] in new_h_edges[p1[1]]
        p2_has_h_support = p2[0] in new_h_edges[p2[1]]

        # Check the conditions for being a rear left placement point
        if p1_has_v_support and not p1_has_h_support and p1 not in active_points:
            active_points.append(p1)

        # Check the conditions for being a front right placement point
        if p2_has_h_support and not p2_has_v_support and p2 not in active_points:
            active_points.append(p2)


        new_v_edges[x] |= P.closedopen(y, y + p_w)
        new_v_edges[x + p_l] |= P.closedopen(y, y + p_w)
        new_h_edges[y] |= P.closedopen(x, x + p_l)
        new_h_edges[y + p_w] |= P.closedopen(x, x + p_l)

        return LayerState(
            layer=self.layer.commit_placement(placement), # Layer.commit now returns a new Layer
            warehouse=self.warehouse.delete_piece(placement.get_piece()), # Warehouse.delete now returns new Warehouse
            p_points=tuple(active_points),
            vertical_edges=new_v_edges,
            horizontal_edges=new_h_edges
        )
    
    def get_touching_parameter(self, placement):
        x, y = placement.get_p_point()
        p_w, p_l = placement.get_width(), placement.get_length()
        tp = 0

        # Calculate interval intersections
        tp += self._measure(P.closedopen(x, x + p_l) & self.horizontal_edges[y])
        tp += self._measure(P.closedopen(y, y + p_w) & self.vertical_edges[x])
        tp += self._measure(P.closedopen(x, x + p_l) & self.horizontal_edges[y + p_w])
        tp += self._measure(P.closedopen(y, y + p_w) & self.vertical_edges[x + p_l])
        
        return tp

    def _measure(self, interval):
        return sum(i.upper - i.lower for i in interval) if not interval.empty else 0

    def __eq__(self, other):
        if not isinstance(other, LayerState): return False
        return self._cached_hash == other._cached_hash

    def __hash__(self):
        return self._cached_hash