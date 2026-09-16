import numpy as np 

class Solution:
        # we want the counts of all the atoms in a dict
    elements = ('H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F',
                'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
                'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni',
                'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
                'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag',
                'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Hf',
                'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
                'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 
                'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og', 'Ce',
                'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm',
                'Yb', 'Lu', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf',
                'Es', 'Fm', 'Md', 'No', 'Lr')

    def multiply(self, d, m):
        for k in d.keys():
            d[k] *= m
        return d

    def parse_numbers(self, elements, i):
        num = ""
        while i < len(elements):
            if elements[i].isalpha() or elements[i]== '(' or elements[i] == ')' or elements[i] == len(elements):
                return int(num), i
            num += elements[i]
            i+=1
        return int(num), i

    def parse_letters(self, elements, i):
        output = ""
        while i < len(elements):
            if not (elements[i].islower() and elements[i].isalpha()) or elements[i] == len(elements):
                return output, i
            output += elements[i]
            i += 1
        return output, i

        

    def helper(self, formula:str, i:str):
        atoms = {}
        while i < len(formula):
            c = formula[i] 
 
            # reading an element
            if c.isupper():
                # Check if it is a double letter elements
                if i + 1 < len(formula) and formula[i + 1].islower():
                    lowers, i = self.parse_letters(formula, i + 1)
                    el = c + lowers
                    i -= 1
                else:
                # Single letter element, check if number is behind it
                    el = c
                
                if i + 1 < len(formula) and formula[i+1].isdigit():
                    num, i = self.parse_numbers(formula, i + 1)
                    if el not in atoms:
                        atoms[el] = num
                    else:
                        atoms[el] += num
                else:
                    i += 1
                    if el not in atoms:
                        atoms[el] = 1
                    else:
                        atoms[el] += 1
                # Check if the number is behind it otherwise one
            elif c == '(':
                sub_dict, i = self.helper(formula, i + 1)
                # clean up the number
                num = 1
                i = i + 1
                if i < len(formula) and formula[i].isdigit():
                    num, i = self.parse_numbers(formula, i)
                self.multiply(sub_dict, num)
                for k in sub_dict.keys():
                    if k not in atoms:
                        atoms[k] = sub_dict[k]
                    else:
                        atoms[k] += sub_dict[k]
            elif c == ')':
                return atoms, i
            else:
                i += 1
        return atoms, i

    def countOfAtomsString(self, formula: str) -> str:
        inner_count, i = self.helper(formula, 0)
        output = ""
        keys = sorted(inner_count.keys())
        for k in keys:
            if inner_count[k] != 1:
                output += k + str(inner_count[k])
            else:
                output += k
        return output

    
    def countOfAtomsDict(self, formula: str) -> dict:
        inner_count, i = self.helper(formula, 0)
        return inner_count

    def balance(self, formula: str) -> str:
        formula = formula.replace(" ", "")
        left, right = formula.split("->")
        old_left = left
        old_right = right
        left = left.split("+")
        right = right.split("+")
        total_molecules = len(right) + len(left)
        left_counts = []
        right_counts = []
        total_counts = set()
        for molecule in left:
            # we want the chemical formula and to create the equations
            counts = self.countOfAtomsDict(molecule)
            left_counts.append((molecule, counts))
            total_counts.update(counts.keys())
        for molecule in right:
            counts = self.countOfAtomsDict(molecule)
            right_counts.append((molecule, counts))
            total_counts.update(counts.keys())
        total_counts = sorted(total_counts)
        matrix = [[0] * total_molecules for i in total_counts]
        for e, element in enumerate(total_counts):
            for i, item in enumerate(left_counts):
                m, c = item
                if element in c:
                    matrix[e][i] = c[element]
            for i, item in enumerate(right_counts):
                m, c = item
                if element in c:
                    matrix[e][i + len(left_counts)] = -c[element]
        print(matrix)
        output = ""
        return output
sol = Solution()
#print(sol.balance('C2H5OH + O2 -> CO2 + H2O'))
print(sol.balance('H2O + O2 -> H2O2'))
