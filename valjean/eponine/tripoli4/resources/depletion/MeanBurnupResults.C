#include "MeanBurnupResults.h"

#include <iostream>

#include "TMath.h"
#include "TAxis.h"

#include <ctime>

ClassImp(MeanBurnupResults);

using namespace std;

void MeanBurnupResults::Initialize(const BurnupResults & result)
{

  steps = result.GetSteps();
  nb_compos = result.GetNbCompos();
  for (int i=0;i<nb_compos;i++)
  {
    compo_names.push_back(result.GetDepletedCompositionName(i+1));
  }
  map<TString,DepletedComposition>::const_iterator it;
  map<TString,double>::iterator it2;
  map<TString,double> mass;
  map<TString,double> concentration;
  map<TString,double> activity;
  map<TString,double> reactionrates;
  map<TString,double> thermal_reactionrates;
  map<TString,double> fast_reactionrates;
  set<TString>::iterator it3;
  set<TString> isotope_names;
  map<TString, set<TString>>::iterator it4;
  map<TString, set<TString>> iso_reac_names;
  compositions.resize(GetSteps());
  for (int i=0; i<GetSteps();i++)
  {
    kcolls.push_back(pair<double,double> (result.kcolls[i],0.));
    ktracks.push_back(pair<double,double> (result.ktracks[i],0.));
    ksteps.push_back(pair<double,double> (result.ksteps[i],0.));
    beff_prompts.push_back(pair<double,double> (result.beff_prompts[i],0.));
    beff_nauchis.push_back(pair<double,double> (result.beff_nauchis[i],0.));
    burnups.push_back(pair<double,double> (result.burnups[i],0.));
    times.push_back(pair<double,double> (result.times[i],0.));
    renorms.push_back(pair<double,double> (result.renorms[i],0.));
    total_powers.push_back(pair<double,double> (result.total_powers[i],0.));
    for (it=result.compositions[i].begin();it!=result.compositions[i].end();it++)
    {
      compositions[i][it->first].resize(2);
      compositions[i][it->first][0].SetName(it->first);
      compositions[i][it->first][0].SetVolume(it->second.GetVolume());
      compositions[i][it->first][0].SetLocalBurnup(it->second.GetLocalBurnup());
      compositions[i][it->first][0].SetPower(it->second.GetPower());
      compositions[i][it->first][0].SetFastFlux(it->second.GetFastFlux());
      compositions[i][it->first][0].SetThermFlux(it->second.GetThermFlux());
      compositions[i][it->first][1].SetName(it->first);
      compositions[i][it->first][1].SetVolume(0.);
      compositions[i][it->first][1].SetLocalBurnup(0.);
      compositions[i][it->first][1].SetPower(0.);
      compositions[i][it->first][1].SetFastFlux(0.);
      compositions[i][it->first][1].SetThermFlux(0.);
      mass = it->second.GetMassMap();
      concentration = it->second.GetConcentrationMap();
      activity = it->second.GetActivityMap();
      reactionrates = it->second.GetReactionRateMap();
      thermal_reactionrates = it->second.GetThermalReactionRateMap();
      fast_reactionrates = it->second.GetFastReactionRateMap();
      isotope_names = it->second.GetIsotopesNames();
      iso_reac_names = it->second.GetIsotopeReactionNames();
      for (it2=mass.begin();it2!=mass.end();++it2)
      {
        compositions[i][it->first][0].SetMass(it2->first,it2->second);
        compositions[i][it->first][1].SetMass(it2->first, 0.);
      }
      for (it2=concentration.begin();it2!=concentration.end();++it2)
      {
        compositions[i][it->first][0].SetConcentration(it2->first,it2->second);
        compositions[i][it->first][1].SetConcentration(it2->first, 0.);
      }
      for (it2=activity.begin();it2!=activity.end();++it2)
      {
        compositions[i][it->first][0].SetActivity(it2->first,it2->second);
        compositions[i][it->first][1].SetActivity(it2->first, 0.);
      }
      for (it2=reactionrates.begin();it2!=reactionrates.end();++it2)
      {
        compositions[i][it->first][0].SetReactionRate(it2->first,it2->second);
        compositions[i][it->first][1].SetReactionRate(it2->first, 0.);
      }
      for (it2=thermal_reactionrates.begin();it2!=thermal_reactionrates.end();++it2)
      {
        compositions[i][it->first][0].SetThermalReactionRate(it2->first,it2->second);
        compositions[i][it->first][1].SetThermalReactionRate(it2->first, 0.);
      }
      for (it2=fast_reactionrates.begin();it2!=fast_reactionrates.end();++it2)
      {
        compositions[i][it->first][0].SetFastReactionRate(it2->first,it2->second);
        compositions[i][it->first][1].SetFastReactionRate(it2->first, 0.);
      }
      for (it3=isotope_names.begin();it3!=isotope_names.end(); ++it3)
      {
        compositions[i][it->first][0].SetIsotopeName(*it3);
        compositions[i][it->first][1].SetIsotopeName(*it3);
      }
      for (it4=iso_reac_names.begin();it4!=iso_reac_names.end(); ++it4)
      {
        for(set<TString>::iterator jt=it4->second.begin(); jt!=it4->second.end(); ++jt) {
          compositions[i][it->first][0].SetIsotopeReactionName(it4->first, *jt);
          compositions[i][it->first][1].SetIsotopeReactionName(it4->first, *jt);
        }
      }
    }
  }
}

void MeanBurnupResults::AddSimulationAndProcess(const char * file_name, const char * tree_name)
{

  BurnupResults temp_bu(file_name,tree_name);
  cout << "Processing file : " << file_name << endl;
  AddSimulationAndProcess(temp_bu);

}

void MeanBurnupResults::AddSimulationAndProcess(const BurnupResults & result)
{

  nb_simus++;
  doubled_nb_simus = (double) nb_simus;
  if (nb_simus==1)
  {
    Initialize(result);
  }
  else
  {
    if (result.GetSteps() != GetSteps())
    {
      cout << "MeanBurnupResults::AddSimu ERROR Simulation " << result.filename << " has a different number of steps..." << endl;
      exit(1);
    }
    double delta(0.);
    map<TString,DepletedComposition>::const_iterator it;
    map<TString,double>::const_iterator it2;
    map<TString,double> mass;
    map<TString,double> concentration;
    map<TString,double> activity;
    map<TString,double> reactionrates;
    map<TString,double> thermal_reactionrates;
    map<TString,double> fast_reactionrates;
    for (int i=0; i<GetSteps();i++)
    {
      delta = result.kcolls[i] - kcolls[i].first;
      kcolls[i].first += delta / doubled_nb_simus;kcolls[i].second += delta * ( result.kcolls[i] - kcolls[i].first);
      delta = result.ktracks[i] - ktracks[i].first;
      ktracks[i].first += delta / doubled_nb_simus;ktracks[i].second += delta * ( result.ktracks[i] - ktracks[i].first);
      delta = result.ksteps[i] - ksteps[i].first;
      ksteps[i].first += delta / doubled_nb_simus;ksteps[i].second += delta * ( result.ksteps[i] - ksteps[i].first);
      delta = result.beff_prompts[i] - beff_prompts[i].first;
      beff_prompts[i].first += delta / doubled_nb_simus;beff_prompts[i].second += delta * ( result.beff_prompts[i] - beff_prompts[i].first);
      delta = result.beff_nauchis[i] - beff_nauchis[i].first;
      beff_nauchis[i].first += delta / doubled_nb_simus;beff_nauchis[i].second += delta * ( result.beff_nauchis[i] - beff_nauchis[i].first);
      delta = result.burnups[i] - burnups[i].first;
      burnups[i].first += delta / doubled_nb_simus;burnups[i].second += delta * ( result.burnups[i] - burnups[i].first);
      delta = result.times[i] - times[i].first;
      times[i].first += delta / doubled_nb_simus;times[i].second += delta * ( result.times[i] - times[i].first);
      delta = result.renorms[i] - renorms[i].first;
      renorms[i].first += delta / doubled_nb_simus;renorms[i].second += delta * ( result.renorms[i] - renorms[i].first);
      delta = result.total_powers[i] - total_powers[i].first;
      total_powers[i].first += delta / doubled_nb_simus;total_powers[i].second += delta * ( result.total_powers[i] - total_powers[i].first);
      for (it=result.compositions[i].begin();it!=result.compositions[i].end();it++)
      {
        delta = it->second.GetVolume() - compositions[i][it->first][0].GetVolume();
        compositions[i][it->first][0].SetVolume(  compositions[i][it->first][0].GetVolume() + delta / doubled_nb_simus);
        compositions[i][it->first][1].SetVolume(  compositions[i][it->first][1].GetVolume() + delta * ( it->second.GetVolume() - compositions[i][it->first][0].GetVolume() ));
        delta = it->second.GetLocalBurnup() - compositions[i][it->first][0].GetLocalBurnup();
        compositions[i][it->first][0].SetLocalBurnup( compositions[i][it->first][0].GetLocalBurnup() + delta / doubled_nb_simus);
        compositions[i][it->first][1].SetLocalBurnup( compositions[i][it->first][1].GetLocalBurnup() + delta * ( it->second.GetLocalBurnup() - compositions[i][it->first][0].GetLocalBurnup() ));
        delta = it->second.GetPower() - compositions[i][it->first][0].GetPower();
        compositions[i][it->first][0].SetPower( compositions[i][it->first][0].GetPower() + delta / doubled_nb_simus);
        compositions[i][it->first][1].SetPower( compositions[i][it->first][1].GetPower() + delta * ( it->second.GetPower() - compositions[i][it->first][0].GetPower() ));
        delta = it->second.GetFastFlux() - compositions[i][it->first][0].GetFastFlux();
        compositions[i][it->first][0].SetFastFlux( compositions[i][it->first][0].GetFastFlux() + delta / doubled_nb_simus);
        compositions[i][it->first][1].SetFastFlux( compositions[i][it->first][1].GetFastFlux() + delta * ( it->second.GetFastFlux() - compositions[i][it->first][0].GetFastFlux()));
        delta = it->second.GetThermFlux() - compositions[i][it->first][0].GetThermFlux();
        compositions[i][it->first][0].SetThermFlux(  compositions[i][it->first][0].GetThermFlux() + delta / doubled_nb_simus);
        compositions[i][it->first][1].SetThermFlux(  compositions[i][it->first][1].GetThermFlux() + delta * ( it->second.GetThermFlux() - compositions[i][it->first][0].GetThermFlux()) );

        mass = it->second.GetMassMap();
        concentration = it->second.GetConcentrationMap();
        activity = it->second.GetActivityMap();
        reactionrates = it->second.GetReactionRateMap();
        thermal_reactionrates = it->second.GetThermalReactionRateMap();
        fast_reactionrates = it->second.GetFastReactionRateMap();
        for (it2=mass.begin();it2!=mass.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetMass(it2->first);
          compositions[i][it->first][0].SetMass(it2->first, compositions[i][it->first][0].GetMass(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetMass(it2->first, compositions[i][it->first][1].GetMass(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetMass(it2->first)) ) ;
        }
        for (it2=concentration.begin();it2!=concentration.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetConcentration(it2->first);
          compositions[i][it->first][0].SetConcentration(it2->first, compositions[i][it->first][0].GetConcentration(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetConcentration(it2->first, compositions[i][it->first][1].GetConcentration(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetConcentration(it2->first)) ) ;
        }
        for (it2=activity.begin();it2!=activity.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetActivity(it2->first);
          compositions[i][it->first][0].SetActivity(it2->first, compositions[i][it->first][0].GetActivity(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetActivity(it2->first, compositions[i][it->first][1].GetActivity(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetActivity(it2->first)) ) ;
        }
        for (it2=reactionrates.begin();it2!=reactionrates.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetReactionRate(it2->first);
          compositions[i][it->first][0].SetReactionRate(it2->first, compositions[i][it->first][0].GetReactionRate(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetReactionRate(it2->first, compositions[i][it->first][1].GetReactionRate(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetReactionRate(it2->first)) ) ;
        }
        for (it2=thermal_reactionrates.begin();it2!=thermal_reactionrates.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetThermalReactionRate(it2->first);
          compositions[i][it->first][0].SetThermalReactionRate(it2->first, compositions[i][it->first][0].GetThermalReactionRate(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetThermalReactionRate(it2->first, compositions[i][it->first][1].GetThermalReactionRate(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetThermalReactionRate(it2->first)) ) ;
        }
        for (it2=fast_reactionrates.begin();it2!=fast_reactionrates.end();it2++)
        {
          delta = it2->second - compositions[i][it->first][0].GetFastReactionRate(it2->first);
          compositions[i][it->first][0].SetFastReactionRate(it2->first, compositions[i][it->first][0].GetFastReactionRate(it2->first) + delta / doubled_nb_simus );
          compositions[i][it->first][1].SetFastReactionRate(it2->first, compositions[i][it->first][1].GetFastReactionRate(it2->first) + delta * ( it2->second - compositions[i][it->first][0].GetFastReactionRate(it2->first)) ) ;
        }
      }
    }
  }
}

void MeanBurnupResults::ClearAll()
{
  steps = 0;
  nb_simus = 0;
  doubled_nb_simus = 0.;
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

double MeanBurnupResults::GetKcoll(int step,int index) const
{

  if (index==0)
    return kcolls[step-1].first;
  else if (index==1)
    return TMath::Sqrt(kcolls[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (kcolls[step-1].first)
      return 100.*TMath::Sqrt(kcolls[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/kcolls[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetKcoll ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetKtrack(int step,int index) const
{

  if (index==0)
    return ktracks[step-1].first;
  else if (index==1)
    return TMath::Sqrt(ktracks[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (ktracks[step-1].first)
      return 100.*TMath::Sqrt(ktracks[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/ktracks[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetKtrack ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetKstep(int step,int index) const
{

  if (index==0)
    return ksteps[step-1].first;
  else if (index==1)
    return TMath::Sqrt(ksteps[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (ksteps[step-1].first)
      return 100.*TMath::Sqrt(ksteps[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/ksteps[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetKstep ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetBeffPrompt(int step,int index) const
{

  if (index==0)
    return beff_prompts[step-1].first;
  else if (index==1)
    return TMath::Sqrt(beff_prompts[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (beff_prompts[step-1].first)
      return 100.*TMath::Sqrt(beff_prompts[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/beff_prompts[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetBeffPrompt ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetBeffNauchi(int step,int index) const
{

  if (index==0)
    return beff_nauchis[step-1].first;
  else if (index==1)
    return TMath::Sqrt(beff_nauchis[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (beff_nauchis[step-1].first)
      return 100.*TMath::Sqrt(beff_nauchis[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/beff_nauchis[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetBeffNauchi ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetBurnup(int step,int index) const
{

  if (index==0)
    return burnups[step-1].first;
  else if (index==1)
    return TMath::Sqrt(burnups[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (burnups[step-1].first)
      return 100.*TMath::Sqrt(burnups[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/burnups[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetBurnup ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetTime(int step,int index) const
{

  if (index==0)
    return times[step-1].first;
  else if (index==1)
    return TMath::Sqrt(times[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (times[step-1].first)
      return 100.*TMath::Sqrt(times[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/times[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetTime ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetRenorm(int step,int index) const
{

  if (index==0)
    return renorms[step-1].first;
  else if (index==1)
    return TMath::Sqrt(renorms[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (renorms[step-1].first)
      return 100.*TMath::Sqrt(renorms[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/renorms[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetRenorm ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetTotalPower(int step,int index) const
{

  if (index==0)
    return total_powers[step-1].first;
  else if (index==1)
    return TMath::Sqrt(total_powers[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)));
  else if (index==2)
  {
    if (total_powers[step-1].first)
      return 100.*TMath::Sqrt(total_powers[step-1].second/(doubled_nb_simus*(doubled_nb_simus-1.)))/total_powers[step-1].first;
    else
      return 0.;
  }
  else
  {
    cout << "MeanBurnupResults::GetTotalPower ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
    exit(1);
  }
}

double MeanBurnupResults::GetPower(int step, TString componame, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetPower WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else {
    if (index==0)
      return (it->second)[0].GetPower();
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetPower()/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetPower())
        return 100.*TMath::Sqrt((it->second)[1].GetPower()/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetPower();
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetPower ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetLocalBurnup(int step, TString componame, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetLocalBurnup WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetLocalBurnup();
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetLocalBurnup()/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetLocalBurnup())
        return 100.*TMath::Sqrt((it->second)[1].GetLocalBurnup()/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetLocalBurnup();
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetLocalBurnup ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetFastFlux(int step, TString componame, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetFastFlux WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetFastFlux();
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetFastFlux()/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetFastFlux())
        return 100.*TMath::Sqrt((it->second)[1].GetFastFlux()/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetFastFlux();
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetFastFlux ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetThermFlux(int step, TString componame, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetThermFlux WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else {
    if (index==0)
      return (it->second)[0].GetThermFlux();
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetThermFlux()/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetThermFlux())
        return 100.*TMath::Sqrt((it->second)[1].GetThermFlux()/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetThermFlux();
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetThermFlux ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetMass(int step, TString componame, TString isoname, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetMass WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetMass(isoname);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetMass(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetMass(isoname))
        return 100.*TMath::Sqrt((it->second)[1].GetMass(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetMass(isoname);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetMass ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetConcentration(int step, TString componame, TString isoname, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetConcentration WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetConcentration(isoname);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetConcentration(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetConcentration(isoname))
        return 100.*TMath::Sqrt((it->second)[1].GetConcentration(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetConcentration(isoname);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetConcentration ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetActivity(int step, TString componame, TString isoname, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetActivity WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetActivity(isoname);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetActivity(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetActivity(isoname))
        return 100.*TMath::Sqrt((it->second)[1].GetActivity(isoname)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetActivity(isoname);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetActivity ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetReactionRate(int step, TString componame, TString isoname, TString reaction, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  TString reac = isoname + reaction ;
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetReactionRate WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetReactionRate(reac);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetReactionRate(reac))
        return 100.*TMath::Sqrt((it->second)[1].GetReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetReactionRate(reac);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetReactionRate ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetThermalReactionRate(int step, TString componame, TString isoname, TString reaction, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  TString reac = isoname + reaction ;
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetThermalReactionRate WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetThermalReactionRate(reac);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetThermalReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetThermalReactionRate(reac))
        return 100.*TMath::Sqrt((it->second)[1].GetThermalReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetThermalReactionRate(reac);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetThermalReactionRate ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

double MeanBurnupResults::GetFastReactionRate(int step, TString componame, TString isoname, TString reaction, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  TString reac = isoname + reaction ;
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetFastReactionRate WARNING Composition " << componame << " is not present..." << endl;
    return 0.;
  }
  else
  {
    if (index==0)
      return (it->second)[0].GetFastReactionRate(reac);
    else if (index==1)
      return TMath::Sqrt((it->second)[1].GetFastReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.)));
    else if (index==2)
    {
      if ((it->second)[0].GetFastReactionRate(reac))
        return 100.*TMath::Sqrt((it->second)[1].GetFastReactionRate(reac)/(doubled_nb_simus*(doubled_nb_simus-1.))) / (it->second)[0].GetFastReactionRate(reac);
      else
        return 0.;
    }
    else
    {
      cout << "MeanBurnupResults::GetFastReactionRate ERROR Unknown index " << index << endl;
      cout << "It should be 0 for mean, 1 for standard error of the mean or 2 relative standard error of the mean" << endl;
      exit(1);
    }
  }
}

DepletedComposition MeanBurnupResults::GetDepletedComposition(int step, TString componame, int index) const
{
  map<TString,vector<DepletedComposition> >::const_iterator it = compositions[step-1].find(componame);
  if (it==compositions[step-1].end())
  {
    cout << "MeanBurnupResults::GetDepletedComposition ERROR Composition " << componame << " is not present..." << endl;
    exit(1);
  }

  if (index==0)
    return (it->second)[0];
  else if (index==1)
  {
    DepletedComposition temp = (it->second)[1];
    temp = temp.Sqrt();
    return temp / TMath::Sqrt(doubled_nb_simus*(doubled_nb_simus-1.));
  }
  else
  {
    cout << "MeanBurnupResults::GetDepletedComposition ERROR Unknown index " << index << endl;
    cout << "It should be 0 for mean or 1 for standard error of the mean" << endl;
    exit(1);
  }

}


void MeanBurnupResults::DumpGlobalResults(int step)
{

  cout << "Dumping results of step = " << step << endl << endl;
  cout << "burnup = " << GetBurnup(step) << "  (" << GetBurnup(step,1) << ")" << endl;
  cout << "time = " << GetTime(step)/86400.<< "  (" << GetTime(step,1)/86400. << ")" << endl;
  cout << "kcoll = " << GetKcoll(step) << "  (" << GetKcoll(step,1)*100000. << "pcm)" << endl;
  cout << "ktrack = " << GetKtrack(step) << "  (" << GetKtrack(step,1)*100000. << "pcm)" << endl;
  cout << "kstep = " << GetKstep(step) << "  (" << GetKstep(step,1)*100000. << "pcm)" << endl;
  cout << "beff_prompt = " << GetBeffPrompt(step) << "  (" << GetBeffPrompt(step,1)*100000. << "pcm)" << endl;
  cout << "beff_nauchi = " << GetBeffNauchi(step) << "  (" << GetBeffNauchi(step,1)*100000. << "pcm)" << endl;
  cout << "renorm = " << GetRenorm(step) << "  (" << GetRenorm(step,1) << ")" << endl;
  cout << "total_power = " << GetTotalPower(step) << "  (" << GetTotalPower(step,1) << ")" << endl;
  cout << "Number of depleted compositions = " << compositions[step-1].size() << endl;
  map<TString,vector<DepletedComposition> >::iterator it;
  for (it=compositions[step-1].begin();it!=compositions[step-1].end();it++) {
    cout << "Dumping mean results for composition :  " << it->first << endl;
    it->second[0].DumpGlobals();
  }

}

TGraphErrors* MeanBurnupResults::GetKcollGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKcoll(i+1));
    gr->SetPointError(i,0,GetKcoll(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{coll}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetKtrackGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKtrack(i+1));
    gr->SetPointError(i,0,GetKtrack(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{track}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetKstepGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetKstep(i+1));
    gr->SetPointError(i,0,GetKstep(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("k_{step}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetBeffPromptGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetBeffPrompt(i+1));
    gr->SetPointError(i,0,GetBeffPrompt(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("#Beta_{eff prompt}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetBeffNauchiGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetBeffNauchi(i+1));
    gr->SetPointError(i,0,GetBeffNauchi(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("#Beta_{eff Nauchi}");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetRenormGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetRenorm(i+1));
    gr->SetPointError(i,0,GetRenorm(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Renorm");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetTotalPowerGraph(int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetTotalPower(i+1));
    gr->SetPointError(i,0,GetTotalPower(i+1,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Total Power [W]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetPowerGraph(TString componame, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetPower(i+1,componame));
    gr->SetPointError(i,0,GetPower(i+1,componame,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Power [W]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetLocalBurnupGraph(TString componame, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetLocalBurnup(i+1,componame));
    gr->SetPointError(i,0,GetLocalBurnup(i+1,componame,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("LocalBurnup [MWd/t]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetFluxGraph(TString componame, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetFastFlux(i+1,componame)+GetThermFlux(i+1,componame));
    gr->SetPointError(i,0,TMath::Sqrt(GetFastFlux(i+1,componame,1)*GetFastFlux(i+1,componame,1)+GetThermFlux(i+1,componame,1)*GetThermFlux(i+1,componame,1)));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetFastFluxGraph(TString componame, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetFastFlux(i+1,componame));
    gr->SetPointError(i,0,GetFastFlux(i+1,componame,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Fast Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetThermFluxGraph(TString componame, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetThermFlux(i+1,componame));
    gr->SetPointError(i,0,GetThermFlux(i+1,componame,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Therm Flux");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetMassGraph(TString componame, TString isotope, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0) {
      x = GetBurnup(i+1);
      }
    else {
      x = GetTime(i+1)/86400.;
      }
    gr->SetPoint(i,x,GetMass(i+1,componame,isotope));
    gr->SetPointError(i,0,GetMass(i+1,componame,isotope,1));
  }

  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Mass [g]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();

  return gr;

}

TGraphErrors* MeanBurnupResults::GetConcentrationGraph(TString componame, TString isotope, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1)/86400.;
    gr->SetPoint(i,x,GetConcentration(i+1,componame,isotope));
    gr->SetPointError(i,0,GetConcentration(i+1,componame,isotope,1));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Concentration [10^{-24}at.cm^{-3}]");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraphErrors* MeanBurnupResults::GetActivityGraph(TString componame, TString isotope, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1)/86400.;
    gr->SetPoint(i,x,GetActivity(i+1,componame,isotope));
    gr->SetPointError(i,0,GetActivity(i+1,componame,isotope,1));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle("Activity");
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraphErrors* MeanBurnupResults::GetReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1)/86400.;
    gr->SetPoint(i,x,GetReactionRate(i+1,componame,isotope,reaction));
    gr->SetPointError(i,0,GetReactionRate(i+1,componame,isotope,reaction,1));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraphErrors* MeanBurnupResults::GetThermalReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1)/86400.;
    gr->SetPoint(i,x,GetThermalReactionRate(i+1,componame,isotope,reaction));
    gr->SetPointError(i,0,GetThermalReactionRate(i+1,componame,isotope,reaction,1));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

TGraphErrors* MeanBurnupResults::GetFastReactionRateGraph(TString componame, TString isotope, TString reaction, int index) const
{

  const Int_t n_steps = GetSteps();
  TGraphErrors * gr = new TGraphErrors(n_steps);
  for (int i=0;i<n_steps;i++) {
    double x = 0.;
    if (index==0)
      x = GetBurnup(i+1);
    else
      x = GetTime(i+1)/86400.;
    gr->SetPoint(i,x,GetFastReactionRate(i+1,componame,isotope,reaction));
    gr->SetPointError(i,0,GetFastReactionRate(i+1,componame,isotope,reaction,1));
  }
  if (index==0) gr->GetXaxis()->SetTitle("Burnup [MWd/t]");
  else gr->GetXaxis()->SetTitle("Time [d]");
  gr->GetYaxis()->SetTitle(isotope+reaction);
  gr->GetXaxis()->CenterTitle();
  gr->GetYaxis()->CenterTitle();
  return gr;

}

Histogram MeanBurnupResults::GetKcollHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetKcoll(i+1);
    thist.errors[i] = GetKcoll(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "kcoll";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetKtrackHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetKtrack(i+1);
    thist.errors[i] = GetKtrack(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "ktrack";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetKstepHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetKstep(i+1);
    thist.errors[i] = GetKstep(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "kstep";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetBeffPromptHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetBeffPrompt(i+1);
    thist.errors[i] = GetBeffPrompt(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "beff_prompt";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetBeffNauchiHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetBeffNauchi(i+1);
    thist.errors[i] = GetBeffNauchi(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "beff_nauchi";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetRenormHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetRenorm(i+1);
    thist.errors[i] = GetRenorm(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "renorm";
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetTotalPowerHistogram(int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetTotalPower(i+1);
    thist.errors[i] = GetTotalPower(i+1, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "total_power";
  thist.yunit = "W";
  return thist;
}

Histogram MeanBurnupResults::GetPowerHistogram(TString componame, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetPower(i+1, componame);
    thist.errors[i] = GetPower(i+1, componame, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "power";
  thist.yunit = "W";
  return thist;
}

Histogram MeanBurnupResults::GetLocalBurnupHistogram(TString componame, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetLocalBurnup(i+1, componame);
    thist.errors[i] = GetLocalBurnup(i+1, componame, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "local_burnup";
  thist.yunit = "MWd/t";
  return thist;
}

Histogram MeanBurnupResults::GetFluxHistogram(TString componame, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetFastFlux(i+1, componame) + GetThermFlux(i+1, componame);
    thist.errors[i] = TMath::Sqrt(GetFastFlux(i+1, componame, 1)*GetFastFlux(i+1, componame, 1)
                                  + GetThermFlux(i+1, componame, 1)*GetThermFlux(i+1, componame, 1));
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "flux";
  thist.yunit = "cm-2.s-1";
  return thist;
}

Histogram MeanBurnupResults::GetFastFluxHistogram(TString componame, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetFastFlux(i+1, componame);
    thist.errors[i] = GetFastFlux(i+1, componame, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "fast_flux";
  thist.yunit = "cm-2.s-1";
  return thist;
}

Histogram MeanBurnupResults::GetThermFluxHistogram(TString componame, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetThermFlux(i+1, componame);
    thist.errors[i] = GetThermFlux(i+1, componame, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "thermal_flux";
  thist.yunit = "cm-2.s-1";
  return thist;
}

Histogram MeanBurnupResults::GetMassHistogram(TString componame, TString isotope, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetMass(i+1, componame, isotope);
    thist.errors[i] = GetMass(i+1, componame, isotope, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "mass";
  thist.yunit = "g";
  return thist;
}

Histogram MeanBurnupResults::GetConcentrationHistogram(TString componame, TString isotope, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetConcentration(i+1, componame, isotope);
    thist.errors[i] = GetConcentration(i+1, componame, isotope, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "concentration";
  thist.yunit = "1e-24at.cm-3";
  return thist;
}

Histogram MeanBurnupResults::GetActivityHistogram(TString componame, TString isotope, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetActivity(i+1, componame, isotope);
    thist.errors[i] = GetActivity(i+1, componame, isotope, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = "activity";
  thist.yunit = "1e-24Bq.cm-3";
  return thist;
}

Histogram MeanBurnupResults::GetReactionRateHistogram(TString componame, TString isotope, TString reaction, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetReactionRate(i+1, componame, isotope, reaction);
    thist.errors[i] = GetReactionRate(i+1, componame, isotope, reaction, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = isotope+reaction;
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetThermalReactionRateHistogram(TString componame, TString isotope, TString reaction, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetThermalReactionRate(i+1, componame, isotope, reaction);
    thist.errors[i] = GetThermalReactionRate(i+1, componame, isotope, reaction, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = isotope+reaction;
  thist.yunit = "";
  return thist;
}

Histogram MeanBurnupResults::GetFastReactionRateHistogram(TString componame, TString isotope, TString reaction, int index) const
{
  const size_t n_steps = GetSteps();
  Histogram thist(n_steps);
  for (size_t i=0;i<n_steps;i++) {
    if (index==0) {
      thist.bins[i] = GetBurnup(i+1);
    } else {
      thist.bins[i] = GetTime(i+1)/86400.;
    }
    thist.values[i] = GetFastReactionRate(i+1, componame, isotope, reaction);
    thist.errors[i] = GetFastReactionRate(i+1, componame, isotope, reaction, 1);
  }
  if (index==0) {
    thist.xname = "burnup";
    thist.xunit = "MWd/t";
  } else {
    thist.xname = "time";
    thist.xunit = "d";
  }
  thist.yname = isotope+reaction;
  thist.yunit = "";
  return thist;
}
