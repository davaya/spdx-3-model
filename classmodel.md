# The Class Model
This document describes the Class method of defining logical data models in a manner that facilitates
defining logical values (the information needed to accomplish a task) and representing logical values
as serialized physical data.

The first obstacle to describing the method is terminology; several terms used are overloaded
or subject to differing opinions as to meaning. Within this document they mean:

## Terminology

* **Class** - the name of a set of features used to distinguish some instances from others.
* **Classifier** - a classification of instances according to their features --- [UML](#uml) Section 9.  
* **Instance** - a logical or physical data item identified by a classifier as being a member of a class.
* **Type** - an exact synonym for class; type and class are used interchangeably.
* **Logical Value** - instances with meaning defined by the model, in the XSD
[Value Space](https://www.w3.org/TR/xmlschema11-2/#value-space).
* **Physical Value** - a sequence of bytes that represents a logical value using a specific data format,
the format-agnostic analog of in the XSD
[Lexical Space](https://www.w3.org/TR/xmlschema11-2/#lexical-space).

In object-oriented programming a class can have public variables, private variables, and methods.
A class model MAY be implemented using OOP classes where logical values are the public variables of a class,
but the class model does not constrain or assume that implementations are OOP-based.

## Principles
1. Every class is based on one of a set of pre-defined root ("base") classes.
2. There are two kinds of base class ([XSD Section 2.2](https://www.w3.org/TR/xmlschema11-1/#concepts-data-model)):
simple ("primitive") and complex ("compound"). Simple class instances are atomic values that
cannot be decomposed, complex class instances are containers
([RDF Section 2.15](https://www.w3.org/TR/REC-rdf-syntax/#section-Syntax-list-elements))
with container type and content.
3. There are two kinds of complex class: datatype and classtype.
    * Datatype ([UML Section 10.2](#uml)) instances are distinguished only by their value.
    * Classtype* instances are distinguished by a subset of their value, called a key or id.

Simple classes are by definition datatypes because there is no subset of a simple instance's
value.  So every class is one of: simple datatype, complex datatype, or complex classtype.

 *\* Classtype is used in this document as the name for "complex class that is not a datatype".
Differing opinions on the meaning of "class" often restrict it to only complex classes, or to only
complex classes that are not datatypes. The class model uses Class as defined in
[RDFS](https://www.w3.org/TR/rdf11-schema/#ch_classes) Section 2:
 "The class of everything. rdfs:Resource is an instance of rdfs:Class"*

## Simple Classes

## Complex Classes

All complex classes have four [multiplicity attributes](#uml) (UML Section 7.5):
* minCount
* maxCount
* isUnique
* isOrdered

|  Container | isUnique | isOrdered |
|-----------:|:--------:|:---------:|
|        Set |   true   |   false   |
| OrderedSet |   true   |   true    |
|   Sequence |  false   |   true    |
|        Bag |  false   |   false   |

Complex classes that enumerate fields by identifier and class must have field identifiers that are
unique within the class (Set or OrderedSet). A complex class may have duplicate field value classes.

In complex classes with no field identifiers, all members have the same value class and the container
may be any of the four container types.


## References
###### [RDF]

*RDF/XML Syntax*, W3C Recommendation, 25 February 2014, https://www.w3.org/TR/rdf-syntax-grammar/

###### [RDFS]

*RDF Schema 1.1*, W3C Recommendation, 25 February 2014, https://www.w3.org/TR/rdf11-schema/

###### [SHACL]

*Shapes Constraint Language (SHACL)*, W3C Recommendation, 20 July 2017, https://www.w3.org/TR/shacl/

###### [UML]

*Unified Modeling Language*, Object Management Group, Version 2.5.1, December 2017,
https://www.omg.org/spec/UML/2.5.1/PDF

###### [XSD]

*W3C XML Schema Definition Language*, 1.1 Part 1, W3C Recommendation 5 April 2012,
https://www.w3.org/TR/xmlschema11-1/