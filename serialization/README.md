# Notes on Serialization

## Serialization info

One approach to serialization is to define a format-specific SPDX data models.
The other is to define an abstract (format-agnostic) SPDX Information Model
along with application-independent serialization rules for each data format.
The information-based approach allows:
1. a single SPDX information model to apply to all serialization formats
2. simple (non-LD) JSON and YAML messages to be defined
3. serialized data in any format to be losslessly converted to, and combined with,
data in any other format.

## Serialization formats

[Information Model](InformationModel) describes the abstract data modeling approach.

The files in this directory provide some notes on the specific serialization formats.

The notes are numbered for easier referencing -- the order is **not** significant.


