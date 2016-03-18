import re

from six.moves.queue import PriorityQueue
from six.moves.html_parser import HTMLParser

from regulations.generator.layers.location_replace import LocationReplace


class LayersApplier(object):
    """ Most layers replace content. We try to do this intelligently here,
    so that layers don't step over each other. """
    HTML_TAG_REGEX = re.compile(r'<[^>]*?>')

    def __init__(self):
        self.queue = PriorityQueue()
        self.text = None

    def enqueue_from_list(self, elements_list):
        for le in elements_list:
            self.enqueue(le)

    def enqueue(self, layer_element):
        original, replacement, locations = layer_element
        priority = len(original)
        item = (original, replacement, locations)
        self.queue.put((-priority, item))

    def location_replace(self, xml_node, original, replacement, locations):
        LocationReplace().location_replace(xml_node, original, replacement,
                                           locations)

    def unescape_text(self):
        """ Because of the way we do replace_all(), we need to unescape HTML
        entities.  """
        self.text = HTMLParser().unescape(self.text)

    def replace_all(self, original, replacement):
        """ Replace all occurrences of original with replacement. This is HTML
        aware; it effectively looks at all of the text in between HTML tags"""
        text_chunks = []
        index = 0
        for match in self.HTML_TAG_REGEX.finditer(self.text):
            text = self.text[index:match.start()]
            text_chunks.append(text.replace(original, replacement))
            text_chunks.append(self.text[match.start():match.end()])    # tag
            index = match.end()
        text_chunks.append(self.text[index:])   # trailing text
        self.text = "".join(text_chunks)
        self.unescape_text()

    def replace_at(self, original, replacement, locations):
        """ Replace the occurrences of original at all the locations with
        replacement. """

        locations.sort()
        self.text = LocationReplace().location_replace_text(
            self.text, original, replacement, locations)
        self.unescape_text()

    def apply_layers(self, original_text):
        self.text = original_text

        while not self.queue.empty():
            priority, layer_element = self.queue.get()
            original, replacement, locations = layer_element

            if not locations:
                self.replace_all(original, replacement)
            else:
                self.replace_at(original, replacement, locations)

        return self.text


class LayersBase(object):
    """ Base class which keeps track of multiple laeyrs. """
    def __init__(self):
        self.layers = {}

    def add_layer(self, layer):
        self.layers[layer.__class__.shorthand] = layer


class SearchReplaceLayersApplier(LayersBase):
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.modified_text = None

    def get_layer_pairs(self, text_index):
        elements = []
        for layer in self.layers.values():
            elements += list(layer.apply_layer(text_index))
        return elements


class InlineLayersApplier(LayersBase):
    """ Apply multiple inline layers to given text (e.g. links,
    highlighting, etc.) """
    def __init__(self):
        LayersBase.__init__(self)
        self.original_text = None
        self.original_text_index = None
        self.modified_text = None

    def get_layer_pairs(self, text_index, original_text):
        layer_pairs = []
        for layer in self.layers.values():
            layer_pairs += list(layer.apply_layer(original_text, text_index))

        # convert from offset-based to a search and replace layer.
        layer_elements = []

        for o, r, offset in layer_pairs:
            offset_locations = LocationReplace.find_all_offsets(o,
                                                                original_text)
            locations = [offset_locations.index(offset)]
            layer_elements.append((o, r, locations))
        return layer_elements


class ParagraphLayersApplier(LayersBase):
    """ Handle layers which apply to the whole paragraph. Layers include
    interpretations, section-by-section analyses, table of contents, etc."""

    def apply_layers(self, node):
        for layer in self.layers.values():
            pair = layer.apply_layer(node['markup_id'])
            if pair:
                node[pair[0]] = pair[1]
        return node
