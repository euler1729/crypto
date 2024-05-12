from BitVector import *

def gf_divide(num, mod, n):
    # Check if the modulus bit pattern is too long
    if mod.length() > n+1:
        raise ValueError("Modulus bit pattern too long")
    
    # Initialize the quotient with zeros and make a deep copy of the dividend for the remainder
    quotient = BitVector( intVal = 0, size = num.length() )
    remainder = num.deep_copy()
    
    # Initialize the loop counter
    i = 0
    
    # Start the division loop
    while 1:
        i = i+1
        
        # Break the loop if we have processed all bits of the dividend
        if (i==num.length()): break
        
        # Determine the highest power of the modulus and remainder
        mod_highest_power = mod.length() - mod.next_set_bit(0) - 1
        if remainder.next_set_bit(0) == -1:
            remainder_highest_power = 0
        else:
            remainder_highest_power = remainder.length() \
                                  - remainder.next_set_bit(0) - 1
        
        # Break the loop if the remainder's highest power is less than the modulus's highest power
        # or if the remainder is zero
        if (remainder_highest_power < mod_highest_power) \
              or int(remainder)==0:
            break
        else: 
            # Calculate the shift for the quotient
            exponent_shift = remainder_highest_power - mod_highest_power
            
            # Update the quotient with the appropriate bit
            quotient[quotient.length() - exponent_shift - 1] = 1
            
            # Create a copy of the modulus and adjust it for multiplication
            quotient_mod_product = mod.deep_copy()
            quotient_mod_product.pad_from_left(remainder.length() - \
                                          mod.length() )
            quotient_mod_product.shift_left(exponent_shift)
            
            # Update the remainder using XOR operation
            remainder = remainder ^ quotient_mod_product
    
    # Trim the remainder to length n if it's longer
    if remainder.length() > n:
        remainder = remainder[remainder.length()-n:]
    
    # Return the quotient and remainder
    return quotient, remainder



def add_polynomials(poly1, poly2):
    return [(a + b) % 2 for a, b in zip(poly1, poly2)]

def subtract_polynomials(poly1, poly2):
    return [(a - b) % 2 for a, b in zip(poly1, poly2)]

def multiply_polynomials(poly1, poly2):
    result = [0] * (len(poly1) + len(poly2) - 1)
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] += poly1[i] * poly2[j]
    return [x % 2 for x in result]


def poly_to_str(poly):
    poly_str = ''
    for i, coeff in enumerate(poly):
        if coeff == 1:
            poly_str += f"x^{len(poly) - i - 1} + "
    if poly_str:
        poly_str = poly_str[:-3]  # Remove trailing '+'
    else:
        poly_str = "0"
    return poly_str

def str_to_poly(poly_str):
    poly = [0] * 8
    if poly_str.strip() == '0':
        return poly
    terms = poly_str.split('+')
    for term in terms:
        term = term.strip()
        if term == '':
            continue
        power = int(term[term.find('^') + 1:])
        poly[7 - power] = 1
    return poly

def toStr(pol):
    res = ''
    for r in pol:
        res += str(r)
    return res

def main():
    mod = BitVector( bitstring = '100011011' ) 
    while True:
        try:
            operand1 = input("Enter the first polynomial as a bit string: ")
            operand2 = input("Enter the second polynomial as a bit string: ")
            operator = input("Enter the operator (+, -, *, /): ")

            if len(operand1) != 8 or len(operand2) != 8:
                raise ValueError("Polynomials must be 8 bits long")

            poly1 = [int(bit) for bit in operand1]
            poly2 = [int(bit) for bit in operand2]

            pol1BV = BitVector(bitstring = operand1)
            pol2BV = BitVector(bitstring = operand2)

            if operator == '+':
                result = add_polynomials(poly1, poly2)
            elif operator == '-':
                result = subtract_polynomials(poly1, poly2)
            elif operator == '*':
                result = multiply_polynomials(poly1, poly2)
            elif operator == '/':
                quotient, remainder = gf_divide(pol1BV, pol2BV, 8)
                print("Quotient:", poly_to_str(quotient))
                print("Remainder:", poly_to_str(remainder))
                continue
            else:
                raise ValueError("Invalid operator")
            if operator !='/':
                bv = BitVector(bitstring = toStr(result))
                q, rem = gf_divide(bv, mod, 8)
                print("Result:", poly_to_str(rem))
                print("Q: ", poly_to_str(q))
        except ValueError as e:
            print("Error:", e)
            continue

        try:
            choice = input("Do you want to continue (y/n)? ")
            if choice.lower() != 'y':
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
