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
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            for field in ['v20state', 'v21town', 'v22general', 'v23town']:
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
        # Apply filters from the form
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            for field in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(field) is True:
                    queryset = queryset.filter(**{field: True})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)
        context['filter_form'] = form

        # Convert queryset to DataFrame for easier aggregation
        queryset = self.get_queryset()
        df = pd.DataFrame.from_records(queryset.values())

        # Debug: Print the election participation columns to check their values
        print("Election Participation Columns:")
        print(df[['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']].head())

        # Graph 1: Distribution of Voters by Year of Birth
        birth_year_counts = df['date_of_birth'].apply(lambda x: x.year).value_counts().sort_index()
        fig1 = go.Figure(data=[go.Bar(x=birth_year_counts.index, y=birth_year_counts.values)])
        fig1.update_layout(title="Distribution of Voters by Year of Birth", xaxis_title="Year", yaxis_title="Count", height = 800, width = 1000)
        context['birth_year_graph'] = plot(fig1, output_type='div')

        # Graph 2: Distribution of Voters by Party Affiliation (Resized)
        party_counts = df['party_affiliation'].value_counts()
        fig2 = go.Figure(data=[go.Pie(labels=party_counts.index, values=party_counts.values)])
        fig2.update_layout(
        title="Distribution of Voters by Party Affiliation",
        width=900,  # Adjust width as needed
        height=900  # Adjust height as needed
        )
        context['party_affiliation_graph'] = plot(fig2, output_type='div')

        # Graph 3: Distribution of Voters by Election Participation
        # Use direct boolean summing for each election column
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [df[election].sum() if election in df else 0 for election in elections]
        
        fig3 = go.Figure(data=[go.Bar(x=elections, y=election_counts)])
        fig3.update_layout(title="Voter Participation by Election", xaxis_title="Election", yaxis_title="Count",
                           height = 800, width = 1000)
        context['election_participation_graph'] = plot(fig3, output_type='div')

        return context
        