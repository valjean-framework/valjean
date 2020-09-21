#ifndef MeanBurnupResults_h
#define MeanBurnupResults_h

#include <vector>
#include <utility>
#include <string>

#include "TObject.h"
#include "TGraphErrors.h"

#include "BurnupResults.h"


struct Histogram {
  Histogram(size_t n_steps) :
    bins{std::vector<double>(n_steps)},
    values{std::vector<double>(n_steps)},
    errors{std::vector<double>(n_steps)} {};
  std::vector<double> bins;
  std::vector<double> values;
  std::vector<double> errors;
  std::string xname;
  std::string xunit;
  std::string yname;
  std::string yunit;
};


class MeanBurnupResults: public TObject {
  private:
    int nb_simus;
    double doubled_nb_simus;
    int nb_compos;
    //
    int steps;
    //
    std::vector<std::pair<double,double> > kcolls;
    std::vector<std::pair<double,double> > ktracks;
    std::vector<std::pair<double,double> > ksteps;
    std::vector<std::pair<double,double> > beff_prompts;
    std::vector<std::pair<double,double> > beff_nauchis;
    std::vector<std::pair<double,double> > burnups;
    std::vector<std::pair<double,double> > times;
    std::vector<std::pair<double,double> > renorms;
    std::vector<std::pair<double,double> > total_powers;

    std::vector<std::map<TString,std::vector<DepletedComposition> > > compositions;
    std::vector< TString > compo_names;

  public:
    MeanBurnupResults() {nb_simus = 0;}

    void AddSimulationAndProcess(const char * file_name, const char * tree_name="evoltree");
    void ClearAll();

    int GetNbSimu() const {return nb_simus;}
    int GetNbCompos() const {return nb_compos;}
    int GetSteps() const {return steps;}
    double GetKcoll(int step,int index=0) const;
    double GetKtrack(int step,int index=0) const;
    double GetKstep(int step,int index=0) const;
    double GetBeffPrompt(int step,int index=0) const;
    double GetBeffNauchi(int step,int index=0) const;
    double GetBurnup(int step,int index=0) const;
    double GetTime(int step,int index=0) const;
    double GetRenorm(int step,int index=0) const;
    double GetTotalPower(int step,int index=0) const;
    double GetPower(int step,TString componame, int index=0) const;
    double GetLocalBurnup(int step,TString componame, int index=0) const;
    double GetFastFlux(int step,TString componame, int index=0) const;
    double GetThermFlux(int step,TString componame, int index=0) const;
    double GetMass(int step,TString componame, TString isotope, int index=0) const;
    double GetConcentration(int step,TString componame, TString isotope, int index=0) const;
    double GetActivity(int step,TString componame, TString isotope, int index=0) const;
    double GetReactionRate(int step,TString componame, TString isotope, TString reaction,int index=0) const;
    double GetThermalReactionRate(int step,TString componame, TString isotope, TString reaction,int index=0) const;
    double GetFastReactionRate(int step,TString componame, TString isotope, TString reaction,int index=0) const;

    DepletedComposition GetDepletedComposition(int step, TString name, int index=0) const;
    const char * GetDepletedCompositionName(int index) const {return compo_names.at(index-1).Data();}
    std::set<TString> GetDepletedIsotopeNames(int index, TString componame) const {
      return compositions.at(index-1).at(componame).at(0).GetIsotopesNames(); }
    std::set<TString> GetDepletedReactionNames(int index, TString componame, TString isotope) const {
      return compositions.at(index-1).at(componame).at(0).GetReactionNames(isotope);}
    std::map<TString, set<TString>> GetDepletedIsotopeReactionNames(int index, TString componame) const {
      return compositions.at(index-1).at(componame).at(0).GetIsotopeReactionNames();}

    TGraphErrors * GetKcollGraph(int index=0) const;
    TGraphErrors * GetKtrackGraph(int index=0) const;
    TGraphErrors * GetKstepGraph(int index=0) const;
    TGraphErrors * GetBeffPromptGraph(int index=0) const;
    TGraphErrors * GetBeffNauchiGraph(int index=0) const;
    TGraphErrors * GetRenormGraph(int index=0) const;
    TGraphErrors * GetTotalPowerGraph(int index=0) const;
    TGraphErrors * GetPowerGraph(TString componame, int index=0) const;
    TGraphErrors * GetLocalBurnupGraph(TString componame, int index=0) const;
    TGraphErrors * GetFluxGraph(TString componame, int index=0) const;
    TGraphErrors * GetFastFluxGraph(TString componame, int index=0) const;
    TGraphErrors * GetThermFluxGraph(TString componame, int index=0) const;
    TGraphErrors * GetMassGraph(TString componame, TString isotope, int index=0) const;
    TGraphErrors * GetConcentrationGraph(TString componame, TString isotope, int index=0) const;
    TGraphErrors * GetActivityGraph(TString componame, TString isotope, int index=0) const;
    TGraphErrors * GetReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;
    TGraphErrors * GetThermalReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;
    TGraphErrors * GetFastReactionRateGraph(TString componame, TString isotope, TString reaction, int index=0) const;

    Histogram GetKcollHistogram(int index=0) const;
    Histogram GetKtrackHistogram(int index=0) const;
    Histogram GetKstepHistogram(int index=0) const;
    Histogram GetBeffPromptHistogram(int index=0) const;
    Histogram GetBeffNauchiHistogram(int index=0) const;
    Histogram GetRenormHistogram(int index=0) const;
    Histogram GetTotalPowerHistogram(int index=0) const;
    Histogram GetPowerHistogram(TString componame, int index=0) const;
    Histogram GetLocalBurnupHistogram(TString componame, int index=0) const;
    Histogram GetFluxHistogram(TString componame, int index=0) const;
    Histogram GetFastFluxHistogram(TString componame, int index=0) const;
    Histogram GetThermFluxHistogram(TString componame, int index=0) const;
    Histogram GetMassHistogram(TString componame, TString isotope, int index=0) const;
    Histogram GetConcentrationHistogram(TString componame, TString isotope, int index=0) const;
    Histogram GetActivityHistogram(TString componame, TString isotope, int index=0) const;
    Histogram GetReactionRateHistogram(TString componame, TString isotope, TString reaction, int index=0) const;
    Histogram GetThermalReactionRateHistogram(TString componame, TString isotope, TString reaction, int index=0) const;
    Histogram GetFastReactionRateHistogram(TString componame, TString isotope, TString reaction, int index=0) const;

    void DumpGlobalResults(int step);

  private:
    void Initialize(const BurnupResults & result);
    void AddSimulationAndProcess(const BurnupResults & result);

  ClassDef(MeanBurnupResults,1);

};
#endif
