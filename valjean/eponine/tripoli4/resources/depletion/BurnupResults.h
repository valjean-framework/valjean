#ifndef BurnupResults_h
#define BurnupResults_h

#include <vector>
#include <map>
#include <iostream>

#include "TObject.h"
#include "TString.h"
#include "TGraph.h"

#include "DepletedComposition.h"

class MeanBurnupResults;

class BurnupResults: public TObject {
  friend class MeanBurnupResults;
  private:
    TString filename;
    TString treename;

    int steps;
    int nb_compos;
    //
    std::vector<double> kcolls;
    std::vector<double> ktracks;
    std::vector<double> ksteps;
    std::vector<double> beff_prompts;
    std::vector<double> beff_nauchis;
    std::vector<double> burnups;
    std::vector<double> times;
    std::vector<double> renorms;
    std::vector<double> total_powers;
    //
    std::vector< std::map< TString, DepletedComposition > > compositions;
    std::vector< TString > compo_names;

  public:
    BurnupResults();
    BurnupResults(const char * file_name, const char * tree_name="evoltree");

    void SetResultFile(const char * file_name, const char * tree_name);
    void SetSteps(int nb_steps) {steps=nb_steps;}

    BurnupResults operator +(const BurnupResults & a);
    BurnupResults operator -(const BurnupResults & a);
    BurnupResults operator *(const BurnupResults & a);
    BurnupResults operator /(double div);

    int GetSteps() const {return steps;}
    int GetNbCompos() const {return nb_compos;}
    double GetKcoll(int step) const {return kcolls.at(step-1);}
    double GetKtrack(int step) const {return ktracks.at(step-1);}
    double GetKstep(int step) const {return ksteps.at(step-1);}
    double GetBeffPrompt(int step) const {return beff_prompts.at(step-1);}
    double GetBeffNauchi(int step) const {return beff_nauchis.at(step-1);}
    double GetBurnup(int step) const {return burnups.at(step-1);}
    double GetTime(int step) const {return times.at(step-1);}
    double GetRenorm(int step) const {return renorms.at(step-1);}
    double GetTotalPower(int step) const {return total_powers.at(step-1);}
    DepletedComposition GetDepletedComposition(int step, TString name) const;
    const char* GetDepletedCompositionName(int index) const {return compo_names.at(index-1).Data();}
    double GetPower(int step,TString componame) const;
    double GetLocalBurnup(int step,TString componame) const;
    double GetFastFlux(int step,TString componame) const;
    double GetThermFlux(int step,TString componame) const;
    double GetMass(int step,TString componame, TString iso) const;
    double GetConcentration(int step,TString componame, TString iso) const;
    double GetActivity(int step,TString componame, TString iso) const;
    double GetReactionRate(int step,TString componame, TString iso, TString reaction) const;
    double GetThermalReactionRate(int step,TString componame, TString iso, TString reaction) const;
    double GetFastReactionRate(int step,TString componame, TString iso, TString reaction) const;


    void DumpGlobalResults();
    void DumpGlobalResults(int step);
    void ClearAll();

    TGraph * GetKcollGraph(int index=0) const;
    TGraph * GetKtrackGraph(int index=0) const;
    TGraph * GetKstepGraph(int index=0) const;
    TGraph * GetBeffPromptGraph(int index=0) const;
    TGraph * GetBeffNauchiGraph(int index=0) const;
    TGraph * GetRenormGraph(int index=0) const;
    TGraph * GetTotalPowerGraph(int index=0) const;
    TGraph * GetPowerGraph(TString componame, int index=0) const;
    TGraph * GetLocalBurnupGraph(TString componame, int index=0) const;
    TGraph * GetFluxGraph(TString componame, int index=0) const;
    TGraph * GetFastFluxGraph(TString componame, int index=0) const;
    TGraph * GetThermFluxGraph(TString componame, int index=0) const;
    TGraph * GetMassGraph(TString componame, TString isotope, int index=0) const;
    TGraph * GetConcentrationGraph(TString componame, TString isotope, int index=0) const;
    TGraph * GetActivityGraph(TString componame, TString isotope, int index=0) const;
    TGraph * GetReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;
    TGraph * GetThermalReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;
    TGraph * GetFastReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;

  private:
    void Process();
    void AddKcoll(double val) {kcolls.push_back(val);}
    void AddKtrack(double val) {ktracks.push_back(val);}
    void AddKstep(double val) {ksteps.push_back(val);}
    void AddBeffPrompt(double val) {beff_prompts.push_back(val);}
    void AddBeffNauchi(double val) {beff_nauchis.push_back(val);}
    void AddBurnup(double val) {burnups.push_back(val);}
    void AddTime(double val) {times.push_back(val);}
    void AddRenorm(double val) {renorms.push_back(val);}
    void AddTotalPower(double val) {total_powers.push_back(val);}
    void AddComposition(std::map<TString, DepletedComposition > val) {compositions.push_back(val);}

  ClassDef(BurnupResults,1);

};
#endif
