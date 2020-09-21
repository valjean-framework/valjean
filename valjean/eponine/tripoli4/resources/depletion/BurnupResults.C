#include "BurnupResults.h"

#include <iostream>
#include <cstdlib>

#include "TFile.h"
#include "TTree.h"
#include "TAxis.h"

ClassImp(BurnupResults);

using namespace std;

BurnupResults::BurnupResults()
{
  steps = 0;
  filename = "";
  treename = "";
}

BurnupResults::BurnupResults(const char * file_name, const char * tree_name)
{
  steps = 0;
  filename = file_name;
  treename = tree_name;

  Process();
}

void BurnupResults::SetResultFile(const char * file_name, const char * tree_name)
{
  filename = file_name;
  treename = tree_name;

  Process();
}

void BurnupResults::Process()
{

  if (filename!=""&&treename!="") {
    Int_t step_num;
    Char_t compo_name[100];
    Char_t isotope_name[10];
    Char_t reaction_name[100];
    Double_t reactionrateg1,reactionrateg2;
    Double_t isotope_conc,mass,activity,powereffect,total_powereffect,renormfact,local_burnup,burnup,cumulirradtime,kcoll,ktrack,kstep,beff_prompt,beff_nauchi,compo_vol,fast_flux, therm_flux;

    TFile* ff = new TFile(filename);
    TTree * TT;
    ff->GetObject(treename,TT);
    //Global results
    TT->SetBranchAddress("step_num", &step_num);
    TT->SetBranchAddress("burnup", &burnup);
    TT->SetBranchAddress("cumulirradtime", &cumulirradtime);
    TT->SetBranchAddress("kcoll", &kcoll);
    TT->SetBranchAddress("ktrack", &ktrack);
    TT->SetBranchAddress("kstep", &kstep);
    TT->SetBranchAddress("beff_prompt", &beff_prompt);
    if(TT->GetListOfBranches()->Contains("beff_nauchy")) {
      TT->SetBranchAddress("beff_nauchy", &beff_nauchi);
    } else {
      TT->SetBranchAddress("beff_nauchi", &beff_nauchi);
    }
    TT->SetBranchAddress("renormfact", &renormfact);
    TT->SetBranchAddress("total_powereffect", &total_powereffect);
    // Composition level results
    TT->SetBranchAddress("compo_name", &compo_name);
    TT->SetBranchAddress("compo_vol", &compo_vol);
    TT->SetBranchAddress("isotope_name", &isotope_name);
    TT->SetBranchAddress("isotope_conc", &isotope_conc);
    TT->SetBranchAddress("activity", &activity);
    TT->SetBranchAddress("mass", &mass);
    TT->SetBranchAddress("local_burnup", &local_burnup);
    TT->SetBranchAddress("reaction_name", &reaction_name);
    TT->SetBranchAddress("reactionrateg1", &reactionrateg1);
    TT->SetBranchAddress("reactionrateg2", &reactionrateg2);
    TT->SetBranchAddress("fast_flux", &fast_flux);
    TT->SetBranchAddress("therm_flux", &therm_flux);
    TT->SetBranchAddress("powereffect", &powereffect);

    Int_t nbx = (Int_t) TT->GetEntries();
    Int_t previous_step = 0;
    TString previous_compo = "";
    TString previous_iso = "";
    TString previous_reaction = "";

    map<TString, DepletedComposition > compos;
    DepletedComposition current_compo;
    TString current_componame;
    TString current_isoname;
    TString current_reactioname;

    cout << "Loading " << filename << endl;

    for (Int_t i=0;i<nbx;i++) {
      TT->GetEntry(i);
      current_componame = compo_name;
      current_isoname = isotope_name;
      current_reactioname = reaction_name;
      if (current_componame!=previous_compo||(step_num!=previous_step&&current_componame==previous_compo)) {
        if (current_compo.GetNumberOfIsotopes()) {
          compos[current_compo.GetCompoName()] = current_compo;
        }
      }
      if (step_num!=previous_step) {
//        cout << "Step number : " << step_num << endl;
        if (compos.size()) {
          AddComposition(compos);
          }
        compos.clear();
        AddKcoll(kcoll);
        AddKtrack(ktrack);
        AddKstep(kstep);
        AddBeffPrompt(beff_prompt);
        AddBeffNauchi(beff_nauchi);
        AddBurnup(burnup);
        AddTime(cumulirradtime);
        AddRenorm(renormfact);
        AddTotalPower(total_powereffect);
      }
      if (current_componame!=previous_compo||(step_num!=previous_step&&current_componame==previous_compo)) {
        current_compo.clear();
        current_compo.SetName(current_componame);
        if (step_num==1) compo_names.push_back(current_componame.Data());
        current_compo.SetVolume(compo_vol);
        current_compo.SetLocalBurnup(local_burnup);
        current_compo.SetPower(powereffect);
        current_compo.SetFastFlux(fast_flux);
        current_compo.SetThermFlux(therm_flux);
      }
      if ((current_isoname!=previous_iso)||(current_isoname==previous_iso&&current_componame!=previous_compo)) {
        current_compo.SetIsotopeName(current_isoname.Data());
        current_compo.SetMass(current_isoname,mass);
        current_compo.SetConcentration(current_isoname,isotope_conc);
        current_compo.SetActivity(current_isoname,activity);
      }
      if (current_reactioname!=previous_reaction
          || ( (current_reactioname==previous_reaction&&previous_iso!=current_isoname) || (current_isoname==previous_iso&&current_componame!=previous_compo) ) ) {
        TString reac = current_isoname+current_reactioname;
        current_compo.SetReactionRate(reac,reactionrateg1+reactionrateg2);
        current_compo.SetThermalReactionRate(reac,reactionrateg2);
        current_compo.SetFastReactionRate(reac,reactionrateg1);
        current_compo.SetIsotopeReactionName(current_isoname.Data(), current_reactioname.Data());
      }
      previous_step = step_num;
      previous_iso = isotope_name;
      previous_compo = compo_name;
      previous_reaction = reaction_name;
    }

    if (current_compo.GetNumberOfIsotopes()) {
      compos[current_compo.GetCompoName()] = current_compo;
    }
    AddComposition(compos);

    nb_compos = compo_names.size();
    steps = previous_step;

    ff->Close();

  }
  else {
    cout << "Result filename and treename are not initialized.Use SetResultFile before..." << endl;
  }
}

void BurnupResults::DumpGlobalResults()
{

  cout << "Number of steps = " << steps << endl << endl;
  for (int i=0;i<steps;i++) {
    cout << i+1 << "\t" << burnups[i] << "\t" << times[i]/86400. << "\t" << kcolls[i] << "\t" << ktracks[i] << "\t" << ksteps[i] << endl;
  }

}

void BurnupResults::DumpGlobalResults(int step)
{

  cout << "Dumping results of step = " << step << endl << endl;
  cout << "burnup = " << GetBurnup(step) << endl;
  cout << "time = " << GetTime(step)/86400. << endl;
  cout << "kcoll = " << GetKcoll(step) << endl;
  cout << "ktrack = " << GetKtrack(step) << endl;
  cout << "kstep = " << GetKstep(step) << endl;
  cout << "beff_prompt = " << GetBeffPrompt(step) << endl;
  cout << "beff_nauchi = " << GetBeffNauchi(step) << endl;
  cout << "renorm = " << GetRenorm(step) << endl;
  cout << "total_power = " << GetTotalPower(step) << endl;
  map<TString, DepletedComposition>::iterator it;
  for (it=compositions[step-1].begin();it!=compositions[step-1].end();it++) {
    it->second.DumpGlobals();
    it->second.DumpMass();
  }

}

void BurnupResults::ClearAll()
{

  filename = "";
  treename = "";
  steps = 0;
  kcolls.clear();
  ktracks.clear();
  ksteps.clear();
  beff_prompts.clear();
  beff_nauchis.clear();
  burnups.clear();
  times.clear();
  renorms.clear();
  total_powers.clear();
  compositions.clear();

}

BurnupResults BurnupResults::operator +(const BurnupResults & a)
{

  if (GetSteps()!=a.GetSteps()) {
    cout << "Operator + cannot be applied on BurnupResults of different sizes " << endl;
    exit(1);
  }

  BurnupResults res;
  map<TString, DepletedComposition >::iterator it;

  res.steps = steps;
  res.kcolls.resize(steps);
  res.ktracks.resize(steps);
  res.ksteps.resize(steps);
  res.beff_prompts.resize(steps);
  res.beff_nauchis.resize(steps);
  res.burnups.resize(steps);
  res.times.resize(steps);
  res.renorms.resize(steps);
  res.total_powers.resize(steps);
  res.compositions.resize(steps);

  for (int i=0;i<steps;i++) {
    res.kcolls[i] = GetKcoll(i+1) + a.GetKcoll(i+1);
    res.ktracks[i] = GetKtrack(i+1) + a.GetKtrack(i+1);
    res.ksteps[i] = GetKstep(i+1) + a.GetKstep(i+1);
    res.beff_prompts[i] = GetBeffPrompt(i+1) + a.GetBeffPrompt(i+1);
    res.beff_nauchis[i] = GetBeffNauchi(i+1) + a.GetBeffNauchi(i+1);
    res.burnups[i] = GetBurnup(i+1) + a.GetBurnup(i+1);
    res.times[i] = GetTime(i+1) + a.GetTime(i+1);
    res.renorms[i] = GetRenorm(i+1) + a.GetRenorm(i+1);
    res.total_powers[i] = GetTotalPower(i+1) + a.GetTotalPower(i+1);
    for (it=compositions[i].begin();it!=compositions[i].end();it++) {
      res.compositions[i][it->first] = GetDepletedComposition(i+1,it->first) + a.GetDepletedComposition(i+1,it->first);
    }
  }

  return res;

}

BurnupResults BurnupResults::operator -(const BurnupResults & a)
{

  if (GetSteps()!=a.GetSteps()) {
    cout << "Operator - cannot be applied on BurnupResults of different sizes " << endl;
    exit(1);
  }

  BurnupResults res;
  map<TString, DepletedComposition >::iterator it;

  res.steps = steps;
  res.kcolls.resize(steps);
  res.ktracks.resize(steps);
  res.ksteps.resize(steps);
  res.beff_prompts.resize(steps);
  res.beff_nauchis.resize(steps);
  res.burnups.resize(steps);
  res.times.resize(steps);
  res.renorms.resize(steps);
  res.total_powers.resize(steps);
  res.compositions.resize(steps);

  for (int i=0;i<steps;i++) {
    res.kcolls[i] = GetKcoll(i+1) - a.GetKcoll(i+1);
    res.ktracks[i] = GetKtrack(i+1) - a.GetKtrack(i+1);
    res.ksteps[i] = GetKstep(i+1) - a.GetKstep(i+1);
    res.beff_prompts[i] = GetBeffPrompt(i+1) - a.GetBeffPrompt(i+1);
    res.beff_nauchis[i] = GetBeffNauchi(i+1) - a.GetBeffNauchi(i+1);
    res.burnups[i] = GetBurnup(i+1) - a.GetBurnup(i+1);
    res.times[i] = GetTime(i+1) - a.GetTime(i+1);
    res.renorms[i] = GetRenorm(i+1) - a.GetRenorm(i+1);
    res.total_powers[i] = GetTotalPower(i+1) - a.GetTotalPower(i+1);
    for (it=compositions[i].begin();it!=compositions[i].end();it++) {
      res.compositions[i][it->first] = GetDepletedComposition(i+1,it->first) - a.GetDepletedComposition(i+1,it->first);
    }
  }

  return res;

}

BurnupResults BurnupResults::operator *(const BurnupResults & a)
{

  if (GetSteps()!=a.GetSteps()) {
    cout << "Operator * cannot be applied on BurnupResults of different sizes " << endl;
    exit(1);
  }

  BurnupResults res;
  map<TString, DepletedComposition >::iterator it;

  res.steps = steps;
  res.kcolls.resize(steps);
  res.ktracks.resize(steps);
  res.ksteps.resize(steps);
  res.beff_prompts.resize(steps);
  res.beff_nauchis.resize(steps);
  res.burnups.resize(steps);
  res.times.resize(steps);
  res.renorms.resize(steps);
  res.total_powers.resize(steps);
  res.compositions.resize(steps);

  for (int i=0;i<steps;i++) {
    res.kcolls[i] = GetKcoll(i+1) * a.GetKcoll(i+1);
    res.ktracks[i] = GetKtrack(i+1) * a.GetKtrack(i+1);
    res.ksteps[i] = GetKstep(i+1) * a.GetKstep(i+1);
    res.beff_prompts[i] = GetBeffPrompt(i+1) * a.GetBeffPrompt(i+1);
    res.beff_nauchis[i] = GetBeffNauchi(i+1) * a.GetBeffNauchi(i+1);
    res.burnups[i] = GetBurnup(i+1) * a.GetBurnup(i+1);
    res.times[i] = GetTime(i+1) * a.GetTime(i+1);
    res.renorms[i] = GetRenorm(i+1) * a.GetRenorm(i+1);
    res.total_powers[i] = GetTotalPower(i+1) * a.GetTotalPower(i+1);
    for (it=compositions[i].begin();it!=compositions[i].end();it++) {
      res.compositions[i][it->first] = GetDepletedComposition(i+1,it->first) * a.GetDepletedComposition(i+1,it->first);
    }
  }

  return res;

}

BurnupResults BurnupResults::operator /(double div)
{
  if (div==0.) {
    cout << "Division by 0 ..." << endl;
    exit(1);
  }

  BurnupResults res;
  map<TString, DepletedComposition >::iterator it;

  res.steps = steps;
  res.kcolls.resize(steps);
  res.ktracks.resize(steps);
  res.ksteps.resize(steps);
  res.beff_prompts.resize(steps);
  res.beff_nauchis.resize(steps);
  res.burnups.resize(steps);
  res.times.resize(steps);
  res.renorms.resize(steps);
  res.total_powers.resize(steps);
  res.compositions.resize(steps);

  for (int i=0;i<steps;i++) {
    res.kcolls[i] = GetKcoll(i+1) / div;
    res.ktracks[i] = GetKtrack(i+1) / div;
    res.ksteps[i] = GetKstep(i+1) / div;
    res.beff_prompts[i] = GetBeffPrompt(i+1) / div;
    res.beff_nauchis[i] = GetBeffNauchi(i+1) / div;
    res.burnups[i] = GetBurnup(i+1) / div;
    res.times[i] = GetTime(i+1) / div;
    res.renorms[i] = GetRenorm(i+1) / div;
    res.total_powers[i] = GetTotalPower(i+1) / div;
    for (it=compositions[i].begin();it!=compositions[i].end();it++) {
      res.compositions[i][it->first] = GetDepletedComposition(i+1,it->first) / div;
    }
  }

  return res;

}

DepletedComposition BurnupResults::GetDepletedComposition(int step, TString name) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(name);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetDepletedComposition ERROR Composition " << name << " is not present..." << endl;
    exit(1);
  }
  return it->second;
}

double BurnupResults::GetPower(int step,TString componame) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetPower WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetPower();
}

double BurnupResults::GetLocalBurnup(int step,TString componame) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetLocalBurnup WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetLocalBurnup();
}

double BurnupResults::GetFastFlux(int step,TString componame) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetFastFlux WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetFastFlux();
}

double BurnupResults::GetThermFlux(int step,TString componame) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetThermFlux WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetThermFlux();
}

double BurnupResults::GetMass(int step,TString componame, TString iso) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetMass WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetMass(iso);
}

double BurnupResults::GetConcentration(int step,TString componame, TString iso) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetConcentration WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetConcentration(iso);
}

double BurnupResults::GetActivity(int step,TString componame, TString iso) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetActivity WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetActivity(iso);
}

double BurnupResults::GetReactionRate(int step,TString componame, TString iso, TString reaction) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetReactionRate WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetReactionRate(iso+reaction);
}

double BurnupResults::GetThermalReactionRate(int step,TString componame, TString iso, TString reaction) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetReactionRate WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetThermalReactionRate(iso+reaction);
}

double BurnupResults::GetFastReactionRate(int step,TString componame, TString iso, TString reaction) const
{
  map<TString,DepletedComposition>::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end()) {
    cout << "BurnupResults::GetReactionRate WARNING Composition " << componame << " is not present..." << endl;
  }
  return it==compositions[step-1].end() ? 0. : it->second.GetFastReactionRate(iso+reaction);
}

TGraph* BurnupResults::GetKcollGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKcoll(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{coll}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetKtrackGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKtrack(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{track}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetKstepGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKstep(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{step}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetBeffPromptGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetBeffPrompt(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("#Beta_{eff prompt}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetBeffNauchiGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetBeffNauchi(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("#Beta_{eff Nauchi}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetRenormGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetRenorm(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Renorm");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetTotalPowerGraph(int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetTotalPower(i+1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Total Power [W]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetPowerGraph(TString componame, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetPower(i+1,componame));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Power [W]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetLocalBurnupGraph(TString componame, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetLocalBurnup(i+1,componame));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("LocalBurnup [MWd/t]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetFluxGraph(TString componame, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetFastFlux(i+1,componame)+GetThermFlux(i+1,componame));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetFastFluxGraph(TString componame, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetFastFlux(i+1,componame));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Fast Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetThermFluxGraph(TString componame, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetThermFlux(i+1,componame));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Therm Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetMassGraph(TString componame, TString isotope, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetMass(i+1,componame,isotope));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Mass [g]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraph* BurnupResults::GetConcentrationGraph(TString componame, TString isotope, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1);
    gr->SetPoint(i,x,GetConcentration(i+1,componame,isotope));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Mass [g]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraph* BurnupResults::GetActivityGraph(TString componame, TString isotope, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1);
    gr->SetPoint(i,x,GetActivity(i+1,componame,isotope));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Activity");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraph* BurnupResults::GetReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1);
    gr->SetPoint(i,x,GetReactionRate(i+1,componame,isotope,reaction));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraph* BurnupResults::GetThermalReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1);
    gr->SetPoint(i,x,GetThermalReactionRate(i+1,componame,isotope,reaction));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraph* BurnupResults::GetFastReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  TGraph * gr = new TGraph();
  for (int i=0;i<GetSteps();i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1);
    gr->SetPoint(i,x,GetFastReactionRate(i+1,componame,isotope,reaction));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}
