from genson import SchemaBuilder
from genson.schema.strategies import SchemaStrategy, List


class StrictTypeSchema(SchemaStrategy):
    """ Adds new strategy to Genson schema generation.

    The Strategy is to add const to the fields, so it is a strict validation. In case
    of array items, enum will be added instead for each unique value inside list.

    Attributes:
        JS_TYPES (tuple): Tuple of types to write to the schema
        PYTHON_TYPES (tuple): Tuple of python data types to match the current value from.
            If the type of the current object matches a type in PYTHON_TYPES this
            strategy will be applied.
        KEYWORDS (tuple): Tuple of keywords to use in schema construction, inherits type,
            const and enum is added.
        const (Any): Value of the object to be written to the
            schema
        enum (list): List of consts that will be written to the schema
        type (Any): Type of the const that will be written the schema
    """
    JS_TYPES = ('integer', 'number', 'boolean', 'string')
    PYTHON_TYPES = (int, float, bool, str)
    KEYWORDS = (*SchemaStrategy.KEYWORDS, 'const', 'enum')

    @classmethod
    def match_schema(cls, schema: dict) -> bool:
        """Check if schema type is in strategy"""
        return schema.get('type') in cls.JS_TYPES

    @classmethod
    def match_object(cls, obj):
        """Check if python type of object matches strategy types"""
        return type(obj) in cls.PYTHON_TYPES

    def __init__(self, node_class):
        super().__init__(node_class)
        self.const = None
        self.enum = []
        self.type = None

    def add_object(self, obj):
        """Gets the value and type of the object"""
        super().add_object(obj)
        if obj not in self.enum:
            self._add_object_value(obj)
        if not self.type:
            index = self.PYTHON_TYPES.index(type(obj))
            self.type = self.JS_TYPES[index]

    def to_schema(self):
        """Constructs the schema according to the strategy"""
        schema = super().to_schema()
        schema['type'] = self.type
        if self.enum:
            schema['enum'] = self.enum
        else:
            schema['const'] = self.const
        return schema

    def _add_object_value(self, obj):
        if self.enum:
            self.enum.append(obj)
        elif self.const and not self.const == obj:
            self.enum.append(self.const)
            self.enum.append(obj)
        elif self.const:
            self.enum.append(self.const)
        else:
            self.const = obj


class StrictListSchema(List):
    """Constructs new strategy to Genson schema generation to include minItems to arrays.

    Attributes:
        count (int): The length of the array. Will be written to minItems in the schema
    """

    def __init__(self, node_class):
        super().__init__(node_class)
        self.count = None

    def add_object(self, obj):
        """Gets the length of the array"""
        for item in obj:
            self._items.add_object(item)
        self.count = len(obj)

    def to_schema(self):
        """Constructs the schema according to the strategy"""
        schema = super().to_schema()
        schema['type'] = 'array'
        if self._items:
            schema['items'] = self.items_to_schema()
            schema['minItems'] = self.count
        return schema


class StrictSchemaBuilder(SchemaBuilder):
    """ Strict Schema Builder inherits the SchemaBuilder and adds two new strategies

    The Strategies is to add const to the fields, so it is a strict validation. In case
    of array items, enum will be added instead for each unique value inside list also
    the minimum amount of elements will be added to the schema for the array.

    Attributes:
        EXTRA_STRATEGIES (tuple): Tuple of strategies to use when generating schema
    """
    EXTRA_STRATEGIES = (StrictListSchema, StrictTypeSchema,)
