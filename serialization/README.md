# Notes on Serialization

## Information Model

One serialization approach is to define a format-specific SPDX data model for
each supported data format.

The other is to define an abstract SPDX Information Model (IM) along with universal
serialization rules that bind any IM to serializations for each supported data format.
The information-based approach allows:
1. a single SPDX information model to apply to all serialization formats
2. simple (non-LD) JSON and YAML messages to be defined
3. serialized data in any format to be losslessly converted to, and combined with,
data in any other format.

[Information Model](InformationModel) describes the abstract data modeling approach.

## Serialization formats

The files in this directory provide some notes on the specific serialization formats.

The notes are numbered for easier referencing -- the order is **not** significant.

## Use cases

Examples of how to serialize the following cases:
- Person
- Agent
- Annotation
- File
- Package
- Package with ExternalIdentifier
- Package with ExternalReference
- Relationship with Package contains two Files
- Relationship with time properties
- SBOM with two Files
- SpdxDocument with two Files
- SpdxDocument with NamespaceMap
- SpdxDocument with ExternalMap
- Person with no CreationInfo
- Person with minimal CreationInfo
- Person with full CreationInfo
- Bundle
- two Persons
- Bundle of two Persons

- security use cases here

- licensing use cases here

- build use cases here