#ifndef DepletedComposition_h
#define DepletedComposition_h

#include <iostream>
#include <vector>
#include <map>
// #include <string>
#include <set>

#include "TObject.h"
#include "TString.h"

class DepletedComposition: public TObject {
  private:
    TString name;
    double volume;
    double local_burnup;
    double power;
    double fast_flux;
    double therm_flux;
    //
    std::map< TString , double > mass;
    std::map< TString , double > concentration;
    std::map< TString , double > activity;
    std::map< TString , double > reactionrates;
    std::map< TString , double > thermal_reactionrates;
    std::map< TString , double > fast_reactionrates;

    std::set< TString > isotope_names;
    std::map< TString, set<TString> > iso_reac_names;

  public:
    DepletedComposition();

    void clear();

    void SetName(TString componame) {name=componame;}
    void SetVolume(double val) {volume=val;}
    void SetLocalBurnup(double val) {local_burnup=val;}
    void SetPower(double val) {power=val;}
    void SetFastFlux(double val) {fast_flux=val;}
    void SetThermFlux(double val) {therm_flux=val;}
    void SetMass(TString isoname, double val) {mass[isoname]=val;}
    void SetConcentration(TString isoname, double val) {concentration[isoname]=val;}
    void SetActivity(TString isoname, double val) {activity[isoname]=val;}
    void SetReactionRate(TString reac, double val) {reactionrates[reac]=val;}
    void SetThermalReactionRate(TString reac, double val) {thermal_reactionrates[reac]=val;}
    void SetFastReactionRate(TString reac, double val) {fast_reactionrates[reac]=val;}
    void SetIsotopeName(TString isoname) {isotope_names.insert(isoname);}
    void SetIsotopeReactionName(TString isoname, TString reac) {iso_reac_names[isoname].insert(reac);}

    DepletedComposition operator +(const DepletedComposition & a);
    DepletedComposition operator -(const DepletedComposition & a);
    DepletedComposition operator *(const DepletedComposition & a);
    DepletedComposition operator /(double div);
    DepletedComposition Sqrt();

    const char * GetName() const {return name;}
    TString GetCompoName() const {return name;}
    int GetNumberOfIsotopes() const {return (int) mass.size();}
    double GetVolume() const {return volume;}
    double GetLocalBurnup() const {return local_burnup;}
    double GetPower() const {return power;}
    double GetFastFlux() const {return fast_flux;}
    double GetThermFlux() const {return therm_flux;}
    double GetMass(TString isoname) const;
    double GetConcentration(TString isoname) const;
    double GetActivity(TString isoname) const;
    double GetReactionRate(TString reactionname) const;
    double GetThermalReactionRate(TString reactionname) const;
    double GetFastReactionRate(TString reactionname) const;
    std::map<TString, double> GetMassMap() const {return mass;}
    std::map<TString, double> GetConcentrationMap() const {return concentration;}
    std::map<TString, double> GetActivityMap() const {return activity;}
    std::map<TString, double> GetReactionRateMap() const {return reactionrates;}
    std::map<TString, double> GetThermalReactionRateMap() const {return thermal_reactionrates;}
    std::map<TString, double> GetFastReactionRateMap() const {return fast_reactionrates;}

    std::set<TString> GetIsotopesNames() const {return isotope_names;}
    std::map<TString, set<TString>> GetIsotopeReactionNames() const {return iso_reac_names;}
    std::set<TString> GetReactionNames(TString isoname) const {return iso_reac_names.at(isoname);}

    void DumpGlobals() const;
    void DumpMass() const;
    void DumpIsotopes() const;
    void DumpReactionNames() const;

  ClassDef(DepletedComposition,1);

};
#endif
