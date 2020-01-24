import numpy as np
import random
import itertools

class StableMarriage():
    def __init__(self):
        self.emps = []
        self.apps = []

    def n_emps(self):
        return len(self.emps)

    def n_apps(self):
        return len(self.apps)

    def get_emps(self):
        return self.emps
    
    def get_apps(self):
        return self.apps

    def get_emp(self, index):
        if index >= len(self.emps):
            print("Error, employer index", str(index), "out of bounds")
            return -1

        return self.emps[index]

    def get_app(self, index):
        if index >= len(self.apps):
            print("Error, applicant index", str(index), "out of bounds")
            return -1

        return self.apps[index]

    def add_emp(self, emp):
        self.emps.append(emp)

    def add_app(self, app):
        self.apps.append(app)

    def check_validity(self):
        for emp in self.emps:
            assert len(emp.own_prefs) == len(self.apps)

            for aff_pref in emp.aff_prefs:
                assert len(aff_pref) == len(self.emps)

            for app in self.apps:
                assert app in emp.own_prefs
                
                # Only currently functional for 1-1
                for emp2 in self.emps:
                    assert (app, emp2) in emp.tot_prefs


            # Only currently functional for 1-1
            for i, pair1 in enumerate(emp.tot_prefs[:-1]):
                for pair2 in emp.tot_prefs[i+1:]:
                    if pair1[0] == pair2[0]:
                        ind1 = emp.aff_prefs[0].index(pair1[1])
                        ind2 = emp.aff_prefs[0].index(pair2[1])
                        assert ind1 < ind2
                    if pair1[1] == pair2[1]:
                        ind1 = emp.own_prefs.index(pair1[0])
                        ind2 = emp.own_prefs.index(pair2[0])
                        assert ind1 < ind2

            for emp2 in self.emps:
                for aff_pref in emp.aff_prefs:
                    assert emp2 in aff_pref

            

        for app in self.apps:
            assert len(app.prefs) == len(self.emps)

            aff_count = 0

            for emp in self.emps:
                if app in emp.affs:
                    aff_count += 1
                assert emp in app.prefs

            assert aff_count == 1

    def print_marriage(self):

        for i, emp in enumerate(self.emps):
            for aff in emp.affs:
                j = self.apps.index(aff)

                print("Applicant", str(j), "is affiliated with employer", str(i))


        for i, app in enumerate(self.apps):
            pref_indices = [self.emps.index(emp) for emp in app.prefs]

            print("Applicant", str(i), "prefers employers", pref_indices)

        for i, emp in enumerate(self.emps):
            own_pref_indices = [self.apps.index(app) for app in emp.own_prefs]

            print("Employer", str(i), "prefers applicants", own_pref_indices)

            aff_prefs_indices = []

            for j, aff_pref in enumerate(emp.aff_prefs):
                aff_pref_indices = [self.emps.index(emp) for emp in aff_pref]
                aff_prefs_indices.append(aff_pref_indices)

                print("Employer", str(i), "prefers employers", aff_pref_indices, "for its", str(j), "affiliate")


            ind_prefs = [(self.apps.index(pair[0]), self.emps.index(pair[1])) for pair in emp.tot_prefs]
            print("Employer", str(i), "pair prefs:", str(ind_prefs))
            

class Applicant():
    def __init__(self):
        self.prefs = []

    def get_prefs(self):
        if len(self.prefs) == 0:
            print("Error, accessed unset applicant preferences")
            return -1

        return self.prefs

    def set_prefs(self, prefs):
        self.prefs = prefs

    # Does app prefer emp1 to emp2?
    # Currently only works for 1-1
    def prefers(self, emp1, emp2):
        ind1 = self.prefs.index(emp1)
        ind2 = self.prefs.index(emp2)

        return ind1 < ind2

class Employer():
    def __init__(self, affs):
        self.own_prefs = []
        self.aff_prefs = []
        self.tot_prefs = []
        self.affs = affs

    def get_own_prefs(self):
        if len(self.own_prefs) == 0:
            print("Error, accessed unset employer self preferences")
            return -1

        return self.own_prefs

    def get_aff_prefs(self):
        if len(self.aff_prefs) == 0:
            print("Error, accessed unset employer affiliate preferences")
            return -1

        return self.aff_prefs

    def get_tot_prefs(self):
        if len(self.tot_prefs) == 0:
            print("Error, accessed unset employer total preferences")
            return -1

        return self.tot_prefs

    def get_aff_prefs_at(self, index):
        return self.aff_prefs[index]

    def set_own_prefs(self, prefs):
        self.own_prefs = prefs

    def set_tot_prefs(self, prefs):
        self.tot_prefs = prefs

    def add_aff_prefs(self, prefs):
        self.aff_prefs.append(prefs)

    # Does emp prefer match1 to match2?
    # Currently only works for 1-1
    def prefers(self, match1, match2):
        match_set1 = (match1[self], match1[self.affs[0]])
        match_set2 = (match2[self], match2[self.affs[0]])

        match1_ind = self.tot_prefs.index(match_set1)
        match2_ind = self.tot_prefs.index(match_set2)
        
        return match1_ind < match2_ind

def build_marriage(n, version = 'standard', arity = 'one-to-one'):
    if arity == 'one-to-one':
        return build_one_to_one_marriage(n, version)

def build_one_to_one_marriage(n, version):
    marr = StableMarriage()

    for i in range(n):
        app = Applicant()
        marr.add_app(app)

    for i in range(n):
        emp = Employer([marr.get_app(i)])
        own_prefs = marr.get_apps()[i:] + marr.get_apps()[:i]

        if version == 'random':
            own_prefs = list(np.random.permutation(own_prefs))

        emp.set_own_prefs(own_prefs)

        marr.add_emp(emp)

    for i in range(n):
        app = marr.get_app(i)
        prefs = marr.get_emps()[i:] + marr.get_emps()[:i]

        if version == 'random':
            prefs = list(np.random.permutation(prefs))

        app.set_prefs(prefs)

        emp = marr.get_emp(i)
        aff_prefs = marr.get_emps()[i+1:] + marr.get_emps()[:i+1]

        if version == 'random':
            aff_prefs = list(np.random.permutation(prefs))

        emp.add_aff_prefs(aff_prefs)

    for i in range(n):
        emp = marr.get_emp(i)

        tot_prefs = emp.get_own_prefs()        

        for aff_pref in emp.get_aff_prefs():
            tot_prefs = list(itertools.product(tot_prefs, aff_pref))

        # This is a computationally crappy method to randomize
        if version == 'random':
            n_swaps = 100000

            for i in range(n_swaps):
                start_ind = random.randint(0, len(tot_prefs)-1)
                
                for j in range(len(tot_prefs)-1):
                    match1 = tot_prefs[j]
                    match2 = tot_prefs[(j+1)%len(tot_prefs)]

                    match10 = emp.get_own_prefs().index(match1[0])
                    match11 = emp.get_aff_prefs_at(0).index(match1[1])
                    match20 = emp.get_own_prefs().index(match2[0])
                    match21 = emp.get_aff_prefs_at(0).index(match2[1])

                    
                    if match10 > match20 or match11 > match21:
                        tot_prefs[j] = match2
                        tot_prefs[(j+1)%len(tot_prefs)] = match1

        emp.set_tot_prefs(tot_prefs)
        
        
    marr.check_validity()

    return marr

def build_one_to_one(marr, version='standard'):
    if version == 'standard':
        return build_standard_one_to_one(marr)
    if version == 'random':
        return build_random_one_to_one(marr)

def build_standard_one_to_one(marr):
    match = {}

    for i, emp in enumerate(marr.get_emps()):
        app = marr.get_app(i)

        match[emp] = app
        match[app] = emp

    check_one_to_one_validity(marr, match)

    return match

# Testing original gale shapley
# Only 1-1
def gale_shapley(marr):
    temp_prefs = {}
    temp_aff_prefs = {}

    for emp in marr.get_emps():
        temp_prefs[emp] = [app for app in emp.get_own_prefs()]
        temp_aff_prefs[emp] = [emp for emp in emp.get_aff_prefs_at(0)]

    for app in marr.get_apps():
        temp_prefs[app] = [emp for emp in app.get_prefs()]

    queue = [emp for emp in marr.get_emps()] # queue employers
    match = {}

    # Normal DA
    while bool(queue):
        emp = queue.pop(0)
        prop_app = temp_prefs[emp].pop(0)
        print("Employer", str(marr.get_emps().index(emp)), "proposed to Applicant", str(marr.get_apps().index(prop_app)))

        if len(temp_prefs[emp]) == 0:
            temp_prefs.pop(emp)

        if prop_app not in match:
            match[prop_app] = emp
            match[emp] = prop_app
        elif prop_app.prefers(emp, match[prop_app]):
            broken_up_emp = match[prop_app]
            match[prop_app] = emp
            match[emp] = prop_app
            queue.append(broken_up_emp)
        else:
            queue.append(emp)

    if bool(queue):
        print("Queue got emptied")
    
    check_one_to_one_validity(marr, match)
    
    return match
    
def build_random_one_to_one(marr):
    match = {}
    match_inds = np.random.permutation(marr.n_emps())

    for i, emp in  enumerate(marr.get_emps()):
        app = marr.get_app(match_inds[i])

        match[emp] = app
        match[app] = emp

    check_one_to_one_validity(marr, match)

    return match

def check_one_to_one_validity(marr, match):
    for emp in marr.get_emps():
        assert emp in match.keys()
        assert match[match[emp]] == emp

    for app in marr.get_apps():
        assert emp in match.keys()
        assert match[match[app]] == app

def copy_dict(dictionary):
    ret_dict = {}

    for key in dictionary.keys():
        ret_dict[key] = dictionary[key]

    return ret_dict

def print_match(marr, match):
    for a1 in match.keys():
        a2 = match[a1]
        
        if a1 in marr.get_apps():
            print("Applicant", marr.get_apps().index(a1), "is matched with employer", marr.get_emps().index(a2))

def check_one_to_one_stability(marr, match):
    for emp in marr.get_emps():
        for app in marr.get_apps():
            if match[emp] == app:
                continue

            new_match = copy_dict(match)

            emp_match = match[emp]
            app_match = match[app]

            new_match[app] = emp
            new_match[emp] = app
            new_match[emp_match] = app_match
            new_match[app_match] = emp_match

            if app.prefers(emp, app_match) and emp.prefers(new_match, match):
                return False

    return True

def main():
    n_trials = 2000000
    n_instances = 10
    stop = False

    for n_agents in range(4)[3:]:
        if stop: break

        print("Running on " + str(n_agents) + " agents")

        for i in range(n_instances):
            print("Running marriage instance", str(i))
            marr = build_marriage(n_agents, 'random')
            solved = False
            solve_time = -1

            '''
            for j in range(n_trials):
                match = build_one_to_one(marr, 'random')

                if check_one_to_one_stability(marr, match):
                    solved = True
                    solve_time = j + 1
                    break
            '''

            match = gale_shapley(marr)
            
            if check_one_to_one_stability(marr, match):
                print("Yay")
            else:
                print("done fucked")
                marr.print_marriage()
                print_match(marr, match)
                stop = True
                break
   
            ''' 
            if solved:
                print("Solved in", str(solve_time), "trials")
            else:
                print("Unsolved in", str(n_trials), "trials")
                marr.print_marriage()
                stop = True
                break
            '''

if __name__ == '__main__':
    main()
