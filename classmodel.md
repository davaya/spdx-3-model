# The Class Model
This document describes the Class method of defining logical data models in a manner that facilitates
representing logical values as serialized physical data. The first obstacle to describing the
method is terminology; several terms used are heavily overloaded and subject to differing
opinions as to meaning. Within this document they mean:

## Terminology

* Class - the name of a set of features used to distinguish some instances from others.
* Classifier - a classification of instances according to their features --- [UML](#uml) Section 9.  
* Instance - a logical or physical data item identified by a classifier as being a member of a class.
* Class Model - a set of classes.
* Type - an exact synonym for class; type and class are used interchangeably here.
* Value - instances may be logical data values with meaning defined by the model, or physical
data values that represent logical values in a specific data format.

In object-oriented programming a class can have public variables, private variables, and methods.
A class model MAY be implemented using OOP classes where instances are the public variables of a class,
but this document does not constrain or assume that implementations of the class model are OOP-based.

## Principles
1. Every class in a model is based on one of a set of pre-defined root ("core" or "base") classes.
2. There are two kinds of base class: simple ("primitive") and complex ("compound"). Simple classes
cannot be decomposed, compound classes are containers with container type and content.
3. There are two kinds of compound class: [datatype](#uml) Section 10.2 and classtype. Datatype instances
are distinguished only by their value, classtype instances are distinguished by a subset of their value,
known as a "key" or "id".  Simple classes are by definition datatypes because there is no
subset of an instance's atomic value.


## References
###### [UML]

*Unified Modeling Language*, Object Management Group, Version 2.5.1, December 2017,
https://www.omg.org/spec/UML/2.5.1/PDF