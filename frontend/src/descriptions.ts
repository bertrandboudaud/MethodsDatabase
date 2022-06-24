
export class ColumnDescription {
  static getFields() {
    return [
    {
      label: 'action',
      field: 'before'
    },
    {
      field: "id",
      label: "id",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "name",
      label: "name",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    }
  ];}
}

export class CompoundDescription {
  static getFields() {
    return [
    {
      label: 'action',
      field: 'before'
    },
    {
      field: "id",
      label: "id",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "name",
      label: "name",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "iupac",
      label: "iupac",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "method_id",
      label: "method",
      align: "center",
      type: 'string',
      hidden: true,
      editable: true,
      options: function (self) { return self.methods },
      reduce: function (method) { return method.id; }
    },
    {
      field: "method_name",
      label: "method",
      align: "center",
      type: 'string',
      hidden: false,
      editable: false,
      hovered: function(method) {}
    }
  ]}
}

export class EluentDescription {
  static getFields() {
    return [
    {
      label: 'action',
      field: 'before'
    },
    {
      field: "id",
      label: "id",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "name",
      label: "name",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    }
  ]};
}
export class InstrumentDescription {
  static getFields() {
    return [
    {
      label: 'action',
      field: 'before'
    },
    {
      field: "id",
      label: "id",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "name",
      label: "name",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "model",
      label: "model",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    }
  ]};
}

export class MethodDescription {
  static getFields() {
    return [
    {
      label: 'action',
      field: 'before'
    },
    {
      field: "id",
      label: "id",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "name",
      label: "name",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "technique",
      label: "technique",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "comment",
      label: "comment",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "analysis_method",
      label: "analysis_method",
      align: "center",
      type: 'string',
      hidden: false,
      editable: true
    },
    {
      field: "eluent_a_id",
      label: "eluent a",
      align: "center",
      type: 'string',
      hidden: true,
      options: function (self) { return self.eluents },
      reduce: function (eluent) { return eluent.id; },
      editable: true
    },
    {
      field: "eluent_a_name",
      label: "eluent a",
      align: "center",
      type: 'string',
      hidden: false,
      editable: false
    },
    {
      field: "eluent_b_id",
      label: "eluent b",
      align: "center",
      type: 'string',
      hidden: true,
      options: function (self) { return self.eluents },
      reduce: function (eluent) { return eluent.id; },
      editable: true
    },
    {
      field: "eluent_b_name",
      label: "eluent b",
      align: "center",
      type: 'string',
      hidden: false,
      editable: false
    },
    {
      field: "instrument_id",
      label: "instrument",
      align: "center",
      type: 'string',
      hidden: true,
      options: function (self) { return self.instruments },
      reduce: function (instrument) { return instrument.id; },
      editable: true
    },
    {
      field: "instrument_name",
      label: "instrument",
      align: "center",
      type: 'string',
      hidden: true,
      editable: false
    },
    {
      field: "column_id",
      label: "column",
      align: "center",
      type: 'string',
      hidden: true,
      options: function (self) { return self.columns },
      reduce: function (column) { return column.id; },
      editable: true
    },
    {
      field: "column_name",
      label: "column",
      align: "center",
      type: 'string',
      hidden: false,
      editable: false
    },
    {
      field: "lod",
      label: "lod",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "lloq",
      label: "lloq",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "uloq",
      label: "uloq",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "precision",
      label: "precision",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "preferred_sample_volume",
      label: "preferred_sample_volume",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "runtime",
      label: "runtime",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
    {
      field: "price",
      label: "price",
      align: "center",
      type: 'decimal',
      hidden: false,
      editable: true
    },
  ];}
}

