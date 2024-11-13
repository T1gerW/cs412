from django.db import models

from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            # Use icontains to match party affiliation, ignoring trailing spaces
            if form.cleaned_data['party_affiliation']:
                party_affiliation = form.cleaned_data['party_affiliation'].strip()
                queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
    
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=int(form.cleaned_data['min_birth_year']))
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=int(form.cleaned_data['max_birth_year']))
            
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=int(form.cleaned_data['voter_score']))

            # Boolean filters for election participation
            for field in ['v20state', 'v21town','v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field) is True:
                    queryset = queryset.filter(**{field: True})
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context
    
class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'graphs'
    paginate_by = None  # No pagination needed for this view

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            # Use icontains to match party affiliation, ignoring trailing spaces
            if form.cleaned_data['party_affiliation']:
                party_affiliation = form.cleaned_data['party_affiliation'].strip()
                queryset = queryset.filter(party_affiliation__icontains=party_affiliation)
    
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=int(form.cleaned_data['min_birth_year']))
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=int(form.cleaned_data['max_birth_year']))
            
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=int(form.cleaned_data['voter_score']))

            # Boolean filters for election participation
            for field in ['v20state', 'v21town', 'v22general', 'v23town']:
                if form.cleaned_data.get(field) is True:
                    queryset = queryset.filter(**{field: True})
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)
        context['filter_form'] = form

        # Define all fields we want to include
        fields = [
            'date_of_birth', 'party_affiliation', 'voter_score',
            'v20state', 'v21town', 'v21primary', 'v22general', 'v23town'
        ]

        # Retrieve queryset and ensure it includes all specified fields
        queryset = self.get_queryset().values(*fields)
        df = pd.DataFrame.from_records(queryset)

        # Ensure required columns exist, even in an empty DataFrame
        for field in fields:
            if field not in df.columns:
                df[field] = pd.NA if field == 'date_of_birth' else None

        # Graph 1: Distribution of Voters by Year of Birth
        if not df['date_of_birth'].isna().all():
            birth_year_counts = df['date_of_birth'].dropna().apply(lambda x: x.year).value_counts().sort_index()
        else:
            birth_year_counts = pd.Series([])  # empty series for no data
        
        fig1 = go.Figure(data=[go.Bar(x=birth_year_counts.index, y=birth_year_counts.values)])
        fig1.update_layout(title="Distribution of Voters by Year of Birth", xaxis_title="Year", yaxis_title="Count")
        context['birth_year_graph'] = plot(fig1, output_type='div')

        # Graph 2: Distribution of Voters by Party Affiliation
        if not df['party_affiliation'].isna().all():
            party_counts = df['party_affiliation'].value_counts()
        else:
            party_counts = pd.Series([])  # empty series for no data
        
        fig2 = go.Figure(data=[go.Pie(labels=party_counts.index, values=party_counts.values)])
        fig2.update_layout(title="Distribution of Voters by Party Affiliation", width=600, height=600)
        context['party_affiliation_graph'] = plot(fig2, output_type='div')

        # Graph 3: Distribution of Voters by Election Participation
        election_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [df[election].sum() if election in df else 0 for election in election_fields]
        fig3 = go.Figure(data=[go.Bar(x=election_fields, y=election_counts)])
        fig3.update_layout(title="Voter Participation by Election", xaxis_title="Election", yaxis_title="Count")
        context['election_participation_graph'] = plot(fig3, output_type='div')

        return context
